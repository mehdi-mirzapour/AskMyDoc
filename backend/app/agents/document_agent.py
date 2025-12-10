from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langgraph.graph.message import add_messages
from langfuse.callback import CallbackHandler as LangfuseHandler
from langfuse import Langfuse
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
        
        # Initialize Langfuse callback handler and client
        try:
            self.langfuse_handler = LangfuseHandler(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host
            )
            # Initialize Langfuse client for manual tracing
            self.langfuse_client = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host
            )
            logger.info("[bold green]✓ Langfuse integration enabled (with detailed tracing)[/bold green]", extra={"markup": True})
        except Exception as e:
            logger.warning(f"[yellow]⚠ Could not initialize Langfuse: {e}[/yellow]", extra={"markup": True})
            self.langfuse_handler = None
            self.langfuse_client = None
        
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
        
        # Create span for agent node execution if tracing is enabled
        span = None
        if self.langfuse_client and hasattr(self, '_current_trace'):
            span = self._current_trace.span(
                name="agent_reasoning",
                input={"messages": [str(m) for m in messages]},
                metadata={"node": "agent", "iteration": len([m for m in messages if isinstance(m, AIMessage)])}
            )
        
        # Add system message with context
        system_msg = SystemMessage(content="""You are a helpful data analyst assistant. You have access to a database containing Excel data.
        
Your job is to:
1. First, use get_database_schema to understand what tables and columns are available
2. Use execute_sql_query to run SQL queries to answer questions
3. Use check_missing_values when asked about data quality
4. Provide clear, accurate answers based on the data

IMPORTANT SQL GUIDELINES:
1. QUOTING RULES (CRITICAL):
- ALWAYS wrap table and column names in double quotes
- Example: SELECT "Employee Name" FROM "employee.data"
- Required because table names may contain dots or special characters
- Do not quote SQL keywords

2. Aggregation Rules:
- When asked about totals/sums for an entire table or time period, do NOT use GROUP BY
- Example: "What is the total revenue for October 8?" → SELECT SUM(PRICE) FROM "table_8oct" (NO GROUP BY)
- Only use GROUP BY when explicitly asked to break down by categories or compare groups
- Example: "Revenue by product category" → SELECT category, SUM(price) FROM "table" GROUP BY category
- Table names often indicate the time period (e.g., table_8oct = data for Oct 8), so sum the entire table
- Date columns like DATE_OF_ORDER contain individual transaction timestamps, not the reporting period

3. Text Comparisons:
- Always use LOWER() for case-insensitive text comparisons (e.g., WHERE LOWER("column") = 'value')
- This ensures queries work regardless of text casing in the data or user's question

Always explain your reasoning and show the data that supports your answer.""")
        
        full_messages = [system_msg] + list(messages)
        
        # Call LLM with Langfuse callback
        callbacks = [self.langfuse_handler] if self.langfuse_handler else []
        response = self.llm_with_tools.invoke(full_messages, config={"callbacks": callbacks})
        
        # End span if created
        if span:
            span.end(
                output={"response": str(response), "has_tool_calls": bool(self._get_tool_calls(response))}
            )
        
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
        
        # Create span for tools node if tracing is enabled
        tools_span = None
        if self.langfuse_client and hasattr(self, '_current_trace'):
            tools_span = self._current_trace.span(
                name="tools_execution",
                input={"tool_calls": [tc['name'] for tc in tool_calls]},
                metadata={"node": "tools", "num_tools": len(tool_calls)}
            )
        
        # Execute each tool
        outputs = []
        sql_queries = state.get("sql_queries", [])
        
        for tool_call in tool_calls:
            logger.info(f"[bold magenta]⚙️  Executing tool:[/bold magenta] {tool_call['name']} args={tool_call['args']}", extra={"markup": True})
            
            # Create span for individual tool execution
            tool_span = None
            if tools_span:
                tool_span = tools_span.span(
                    name=f"tool_{tool_call['name']}",
                    input=tool_call['args'],
                    metadata={"tool_name": tool_call['name']}
                )
            
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
            
            # End tool span
            if tool_span:
                tool_span.end(output=str(tool_output)[:500])  # Truncate long outputs
        
        # End tools node span
        if tools_span:
            tools_span.end(output={"num_results": len(outputs)})
        
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
        
        # Create Langfuse trace for the entire query
        trace = None
        if self.langfuse_client:
            trace = self.langfuse_client.trace(
                name="agent_query",
                input={"question": question},
                metadata={
                    "model": self.active_model,
                    "agent_type": "langgraph_document_agent"
                }
            )
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=question)],
            "sql_queries": []
        }
        
        # Store trace as instance variable for access in node methods
        if trace:
            self._current_trace = trace
        
        # Run the graph
        try:
            # Create span for graph execution
            graph_span = None
            if trace:
                graph_span = trace.span(
                    name="graph_execution",
                    input={"initial_state": {"question": question}}
                )
            
            final_state = self.graph.invoke(initial_state)
            
            if graph_span:
                graph_span.end(
                    output={
                        "num_messages": len(final_state["messages"]),
                        "sql_queries_executed": len(final_state.get("sql_queries", []))
                    }
                )
            
            # Extract answer from final message
            answer = final_state["messages"][-1].content
            sql_queries = final_state.get("sql_queries", [])
            
            logger.info("[bold green]✓ Question answered successfully[/bold green]", extra={"markup": True})
            
            result = {
                "answer": answer,
                "sql_queries": sql_queries,
                "model": self.active_model
            }
            
            # End trace with result
            if trace:
                trace.update(
                    output=result,
                    metadata={
                        "model": self.active_model,
                        "num_sql_queries": len(sql_queries),
                        "status": "success"
                    }
                )
            
            # Flush Langfuse to ensure trace is sent
            if self.langfuse_client:
                self.langfuse_client.flush()
            
            return result
            
        except Exception as e:
            logger.error(f"[bold red]✗ Error processing question:[/bold red] {e}", extra={"markup": True})
            
            # Update trace with error
            if trace:
                trace.update(
                    output={"error": str(e)},
                    metadata={"status": "error"}
                )
                self.langfuse_client.flush()
            
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
