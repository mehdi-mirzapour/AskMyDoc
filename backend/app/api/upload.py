from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from typing import List
from app.models.schemas import FileUploadResponse, ErrorResponse
from app.core.config import get_settings
from app.core.logger import logger
import shutil

router = APIRouter(prefix="/upload", tags=["upload"])

# This will be set by main.py
excel_processor = None


def set_excel_processor(processor):
    """Set the global excel processor"""
    global excel_processor
    excel_processor = processor


@router.post("/", response_model=FileUploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload Excel files for processing
    
    Args:
        files: List of Excel files to upload
        
    Returns:
        Upload status and metadata
    """
    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(exist_ok=True)
    
    logger.info(f"[bold blue]📤 Uploading {len(files)} file(s)[/bold blue]", extra={"markup": True})
    
    all_tables = []
    total_rows = 0
    
    for file in files:
        # Validate file extension
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}")
        
        # Save file
        file_path = upload_dir / file.filename
        
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process Excel file
            tables = excel_processor.load_excel_file(file_path)
            all_tables.extend(tables)
            
            # Count rows
            for table in tables:
                total_rows += len(excel_processor.tables[table])
            
        except Exception as e:
            logger.error(f"[red]Error processing {file.filename}: {e}[/red]", extra={"markup": True})
            raise HTTPException(status_code=500, detail=str(e))
    
    logger.info(f"[bold green]✓ Successfully uploaded and processed {len(files)} file(s)[/bold green]", extra={"markup": True})
    
    return FileUploadResponse(
        filename=f"{len(files)} files",
        tables_created=all_tables,
        row_count=total_rows,
        status="success"
    )


@router.get("/schema")
async def get_schema():
    """Get the database schema"""
    logger.info("[blue]📋 Fetching database schema[/blue]", extra={"markup": True})
    
    schema = excel_processor.get_schema()
    total_rows = sum(info['row_count'] for info in schema.values())
    
    return {
        "tables": schema,
        "total_tables": len(schema),
        "total_rows": total_rows
    }
