from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest, QuestionResponse, SQLQueryRequest, SQLQueryResponse
from app.core.logger import logger
from datetime import datetime

from app.agents.document_agent import get_agent, reset_agent

router = APIRouter(prefix="/query", tags=["query"])

# This will be set by main.py
excel_processor = None


def set_excel_processor(processor):
    """Set the global excel processor"""
    global excel_processor
    excel_processor = processor


@router.post("/", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about the uploaded documents
    
    Args:
        request: Question request
        
    Returns:
        Answer with metadata
    """
    logger.info(f"[bold yellow]❓ Question received:[/bold yellow] {request.question}", extra={"markup": True})
    
    try:
        # Query the agent
        agent = get_agent()
        result = agent.query(request.question)
        
        return QuestionResponse(
            question=request.question,
            answer=result["answer"],
            sql_queries=result.get("sql_queries"),
            model=result["model"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"[bold red]✗ Error answering question:[/bold red] {e}", extra={"markup": True})
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sql", response_model=SQLQueryResponse)
async def execute_sql(request: SQLQueryRequest):
    """Execute a custom SQL query directly on the database
    
    Args:
        request: SQL query request
        
    Returns:
        Query results with columns and rows
    """
    logger.info(f"[bold magenta]🔧 Direct SQL query:[/bold magenta] {request.query}", extra={"markup": True})
    
    try:
        # Execute the query
        result_df = excel_processor.execute_query(request.query)
        
        # Convert to response format
        columns = result_df.columns.tolist()
        rows = result_df.values.tolist()
        
        logger.info(f"[green]✓ Query executed: {len(rows)} rows returned[/green]", extra={"markup": True})
        
        return SQLQueryResponse(
            query=request.query,
            columns=columns,
            rows=rows,
            row_count=len(rows),
            status="success"
        )
        
    except Exception as e:
        logger.error(f"[bold red]✗ SQL query error:[/bold red] {e}", extra={"markup": True})
        raise HTTPException(status_code=400, detail=f"SQL Error: {str(e)}")


@router.post("/reset")
async def reset_memory():
    """Reset agent memory"""
    reset_agent()
    return {"status": "success", "message": "Agent memory reset"}
