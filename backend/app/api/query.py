from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest, QuestionResponse
from app.core.logger import logger
from datetime import datetime

router = APIRouter(prefix="/query", tags=["query"])

# This will be set by main.py
document_agent = None


def set_document_agent(agent):
    """Set the global document agent"""
    global document_agent
    document_agent = agent


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
        result = document_agent.query(request.question)
        
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
