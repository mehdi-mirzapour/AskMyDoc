from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
from typing import List
import tempfile
from app.models.schemas import AgentExcelResponse
from app.core.logger import logger
from app.agents.document_agent import get_agent
from datetime import datetime

router = APIRouter(prefix="/agent_upload", tags=["agent_upload"])

# This will be set by main.py
excel_processor = None


def set_excel_processor(processor):
    """Set the global excel processor"""
    global excel_processor
    excel_processor = processor


@router.post("/", response_model=AgentExcelResponse)
async def process_upload_query(
    query: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Process uploaded Excel files and answer a query in one request
    
    Args:
        query: User's question (form field)
        files: List of Excel files to upload (form files)
        
    Returns:
        AgentExcelResponse with answer and metadata
    """
    logger.info(f"[bold blue]📤 Agent Upload request:[/bold blue] {len(files)} files, Query: {query}", extra={"markup": True})
    
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    if not query:
        raise HTTPException(status_code=400, detail="No query provided")
    
    temp_files = []
    all_tables = []
    
    try:
        # Process uploaded files
        for idx, file in enumerate(files):
            # Validate file extension
            if not file.filename.endswith(('.xlsx', '.xls')):
                raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}")
            
            logger.info(f"[cyan]📥 Processing file {idx + 1}/{len(files)}:[/cyan] {file.filename}", extra={"markup": True})
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
            content = await file.read()
            temp_file.write(content)
            temp_file.close()
            
            temp_files.append(temp_file.name)
            
            try:
                # Process Excel file
                tables = excel_processor.load_excel_file(Path(temp_file.name))
                all_tables.extend(tables)
                logger.info(f"[green]✓ Created {len(tables)} table(s) from {file.filename}[/green]", extra={"markup": True})
            except Exception as e:
                logger.error(f"[red]Error processing {file.filename}: {e}[/red]", extra={"markup": True})
                raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")
        
        # Execute query
        logger.info(f"[yellow]❓ Executing query:[/yellow] {query}", extra={"markup": True})
        
        try:
            agent = get_agent()
            result = agent.query(query)
            
            logger.info("[bold green]✓ Query executed successfully[/bold green]", extra={"markup": True})
            
            return AgentExcelResponse(
                query=query,
                answer=result["answer"],
                sql_queries=result.get("sql_queries"),
                model=result["model"],
                files_processed=len(files),
                tables_created=all_tables,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"[bold red]✗ Error executing query:[/bold red] {e}", extra={"markup": True})
            raise HTTPException(status_code=500, detail=f"Query execution error: {str(e)}")
    
    finally:
        # Clean up temporary files
        for temp_path in temp_files:
            try:
                Path(temp_path).unlink()
                logger.info(f"[dim]🗑️  Cleaned up temporary file[/dim]", extra={"markup": True})
            except Exception as e:
                logger.warning(f"[yellow]⚠ Failed to delete temp file {temp_path}: {e}[/yellow]", extra={"markup": True})
