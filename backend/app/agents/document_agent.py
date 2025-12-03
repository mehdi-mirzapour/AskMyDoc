from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langgraph.graph.message import add_messages
from langfuse.callback import CallbackHandler as LangfuseHandler
from app.core.config import get_settings
from app.core.logger import logger
from app.agents.tools import tools
import json


class AgentState(TypedDict):
    """State for the agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    sql_queries: list[str]


class DocumentAgent:
    """LangGraph agent for document question answering"""
    
    def __init__(self):
        """Initialize the agent"""
        settings = get_settings()
        
        # Initialize Langfuse callback handler
        try:
            self.langfuse_handler = LangfuseHandler(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host
            )
            logger.info("[bold green]✓ Langfuse integration enabled[/bold green]", extra={"markup": True})
        except Exception as e:
            logger.warning(f"[yellow]⚠ Could not initialize Langfuse: {e}[/yellow]", extra={"markup": True})
            self.langfuse_handler = None
        
        # Initialize LLM based on active model
        self.active_model = settings.active_model
        logger.info(f"[bold cyan]🤖 Initializing AI model:[/bold cyan] {self.active_model}", extra={"markup": True})
        
        if self.active_model == "openai":
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=settings.openai_api_key,
                temperature=0
            )
        elif self.active_model == "mistral":
            self.llm = ChatMistralAI(
                model="mistral-large-latest",
                api_key=settings.mistral_api_key,
                temperature=0
            )
        else:
            raise ValueError(f"Unknown model: {self.active_model}")
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(tools)
        
        # Create tool executor
        self.tool_executor = ToolExecutor(tools)
        
        # Build graph
        self.graph = self._build_graph()
        
        logger.info("[bold green]✓ Document agent initialized successfully[/bold green]", extra={"markup": True})
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", self._call_tools)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        
        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")
        
        return workflow.compile()
    
    def _call_model(self, state: AgentState) -> AgentState:
        """Call the LLM"""
        messages = state["messages"]
        
        # Add system message with context
        system_msg = SystemMessage(content="""You are a helpful data analyst assistant. You have access to a database containing Excel data.
        
Your job is to:
1. First, use get_database_schema to understand what tables and columns are available
2. Use execute_sql_query to run SQL queries to answer questions
3. Use check_missing_values when asked about data quality
4. Provide clear, accurate answers based on the data

IMPORTANT SQL GUIDELINES:
- Always use LOWER() for case-insensitive text comparisons (e.g., WHERE LOWER(column) = 'value')
- This ensures queries work regardless of text casing in the data or user's question
- Example: WHERE LOWER(CARD_TYPE) = 'visa' will match 'Visa', 'VISA', 'visa', etc.

Always explain your reasoning and show the data that supports your answer.""")
        
        full_messages = [system_msg] + list(messages)
        
        # Call LLM with Langfuse callback
        callbacks = [self.langfuse_handler] if self.langfuse_handler else []
        response = self.llm_with_tools.invoke(full_messages, config={"callbacks": callbacks})
        
        return {"messages": [response]}
    
    def _get_tool_calls(self, message: BaseMessage) -> list:
        """Extract tool calls from a message"""
        if isinstance(message, AIMessage):
            # Tool calls are in additional_kwargs for this LangChain version
            tool_calls = message.additional_kwargs.get('tool_calls', [])
            if tool_calls:
                # Convert to the format expected by ToolExecutor
                formatted_calls = []
                for tc in tool_calls:
                    formatted_calls.append({
                        'id': tc.get('id', ''),
                        'name': tc.get('function', {}).get('name', ''),
                        'args': json.loads(tc.get('function', {}).get('arguments', '{}'))
                    })
                return formatted_calls
        return []
    
    def _call_tools(self, state: AgentState) -> AgentState:
        """Execute tools"""
        messages = state["messages"]
        last_message = messages[-1]
        
        # Extract tool calls
        tool_calls = self._get_tool_calls(last_message)
        
        if not tool_calls:
            logger.warning("[yellow]⚠ No tool calls found in message[/yellow]", extra={"markup": True})
            return {"messages": [], "sql_queries": state.get("sql_queries", [])}
        
        # Execute each tool
        outputs = []
        sql_queries = state.get("sql_queries", [])
        
        for tool_call in tool_calls:
            logger.info(f"[bold magenta]⚙️  Executing tool:[/bold magenta] {tool_call['name']}", extra={"markup": True})
            
            # Track SQL queries
            if tool_call['name'] == 'execute_sql_query':
                sql_queries.append(tool_call['args'].get('query', ''))
            
            # Execute tool - ToolExecutor expects ToolInvocation
            tool_invocation = ToolInvocation(
                tool=tool_call['name'],
                tool_input=tool_call['args']
            )
            tool_output = self.tool_executor.invoke(tool_invocation)
            outputs.append(tool_output)
        
        # Create tool messages
        tool_messages = [
            ToolMessage(content=str(output), tool_call_id=tc['id'])
            for tc, output in zip(tool_calls, outputs)
        ]
        
        return {
            "messages": tool_messages,
            "sql_queries": sql_queries
        }
    
    def _should_continue(self, state: AgentState) -> str:
        """Determine if we should continue or end"""
        messages = state["messages"]
        last_message = messages[-1]
        
        # Check if there are tool calls
        tool_calls = self._get_tool_calls(last_message)
        if not tool_calls:
            return "end"
        
        return "continue"
    
    def query(self, question: str) -> dict:
        """Process a question and return the answer
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and metadata
        """
        logger.info(f"[bold yellow]❓ Processing question:[/bold yellow] {question}", extra={"markup": True})
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=question)],
            "sql_queries": []
        }
        
        # Run the graph
        try:
            final_state = self.graph.invoke(initial_state)
            
            # Extract answer from final message
            answer = final_state["messages"][-1].content
            sql_queries = final_state.get("sql_queries", [])
            
            logger.info("[bold green]✓ Question answered successfully[/bold green]", extra={"markup": True})
            
            return {
                "answer": answer,
                "sql_queries": sql_queries,
                "model": self.active_model
            }
            
        except Exception as e:
            logger.error(f"[bold red]✗ Error processing question:[/bold red] {e}", extra={"markup": True})
            raise


# Global agent instance
_agent = None


def get_agent() -> DocumentAgent:
    """Get or create the global agent instance"""
    global _agent
    if _agent is None:
        _agent = DocumentAgent()
    return _agent


def reset_agent():
    """Reset the global agent instance"""
    global _agent
    _agent = None
    logger.info("[bold yellow]🔄 Agent memory reset[/bold yellow]", extra={"markup": True})
