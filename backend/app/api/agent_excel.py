from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import List
import httpx
import tempfile
from app.models.schemas import AgentExcelRequest, AgentExcelResponse
from app.core.logger import logger
from app.agents.document_agent import get_agent
from datetime import datetime

router = APIRouter(prefix="/agent_excel", tags=["agent_excel"])

# This will be set by main.py
excel_processor = None


def set_excel_processor(processor):
    """Set the global excel processor"""
    global excel_processor
    excel_processor = processor


@router.post("/", response_model=AgentExcelResponse)
async def process_excel_query(request: AgentExcelRequest):
    """Process Excel files from URLs and answer a query
    
    Args:
        request: AgentExcelRequest with query and excel_urls
        
    Returns:
        AgentExcelResponse with answer and metadata
    """
    logger.info(f"[bold blue]🔗 Agent Excel request:[/bold blue] {len(request.excel_urls)} URLs, Query: {request.query}", extra={"markup": True})
    
    if not request.excel_urls:
        raise HTTPException(status_code=400, detail="No Excel URLs provided")
    
    if not request.query:
        raise HTTPException(status_code=400, detail="No query provided")
    
    downloaded_files = []
    all_tables = []
    
    try:
        # Download files from URLs
        async with httpx.AsyncClient(timeout=30.0) as client:
            for idx, url in enumerate(request.excel_urls):
                logger.info(f"[cyan]📥 Downloading file {idx + 1}/{len(request.excel_urls)}:[/cyan] {url}", extra={"markup": True})
                
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    
                    # Determine filename from URL or use default
                    filename = url.split("/")[-1]
                    if not filename.endswith(('.xlsx', '.xls')):
                        filename = f"file_{idx + 1}.xlsx"
                    
                    # Save to temporary file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
                    temp_file.write(response.content)
                    temp_file.close()
                    
                    downloaded_files.append((temp_file.name, filename))
                    
                except httpx.HTTPError as e:
                    logger.error(f"[red]Failed to download {url}: {e}[/red]", extra={"markup": True})
                    raise HTTPException(status_code=400, detail=f"Failed to download {url}: {str(e)}")
        
        # Process downloaded files
        for temp_path, original_name in downloaded_files:
            logger.info(f"[blue]📊 Processing:[/blue] {original_name}", extra={"markup": True})
            
            try:
                tables = excel_processor.load_excel_file(Path(temp_path))
                all_tables.extend(tables)
                logger.info(f"[green]✓ Created {len(tables)} table(s) from {original_name}[/green]", extra={"markup": True})
            except Exception as e:
                logger.error(f"[red]Error processing {original_name}: {e}[/red]", extra={"markup": True})
                raise HTTPException(status_code=500, detail=f"Error processing {original_name}: {str(e)}")
        
        # Execute query
        logger.info(f"[yellow]❓ Executing query:[/yellow] {request.query}", extra={"markup": True})
        
        try:
            agent = get_agent()
            result = agent.query(request.query)
            
            logger.info("[bold green]✓ Query executed successfully[/bold green]", extra={"markup": True})
            
            return AgentExcelResponse(
                query=request.query,
                answer=result["answer"],
                sql_queries=result.get("sql_queries"),
                model=result["model"],
                files_processed=len(request.excel_urls),
                tables_created=all_tables,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"[bold red]✗ Error executing query:[/bold red] {e}", extra={"markup": True})
            raise HTTPException(status_code=500, detail=f"Query execution error: {str(e)}")
    
    finally:
        # Clean up temporary files
        for temp_path, _ in downloaded_files:
            try:
                Path(temp_path).unlink()
                logger.info(f"[dim]🗑️  Cleaned up temporary file[/dim]", extra={"markup": True})
            except Exception as e:
                logger.warning(f"[yellow]⚠ Failed to delete temp file {temp_path}: {e}[/yellow]", extra={"markup": True})
