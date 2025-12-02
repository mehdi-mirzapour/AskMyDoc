from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest, QuestionResponse
from app.core.logger import logger
from datetime import datetime

from app.agents.document_agent import get_agent, reset_agent

router = APIRouter(prefix="/query", tags=["query"])


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


@router.post("/reset")
async def reset_memory():
    """Reset agent memory"""
    reset_agent()
    return {"status": "success", "message": "Agent memory reset"}
