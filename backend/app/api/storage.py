"""
API endpoint for uploading files to Azure Blob Storage
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from pydantic import BaseModel

try:
    from app.core.azure_storage import get_uploader
    STORAGE_AVAILABLE = True
except ImportError:
    STORAGE_AVAILABLE = False
    get_uploader = None

from app.core.logger import logger

router = APIRouter(prefix="/api/storage", tags=["storage"])


class UploadResponse(BaseModel):
    """Response for file upload"""
    filename: str
    public_url: str
    size_bytes: int


class MultiUploadResponse(BaseModel):
    """Response for multiple file uploads"""
    files: List[UploadResponse]
    total_files: int


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload a single file to Azure Blob Storage
    
    Args:
        file: File to upload
    
    Returns:
        Public URL of uploaded file
    """
    if not STORAGE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Azure Storage module not available"
        )
    
    uploader = get_uploader()
    
    if not uploader.is_configured():
        raise HTTPException(
            status_code=503,
            detail="Azure Storage not configured. Set AZURE_STORAGE_ACCOUNT and AZURE_STORAGE_KEY environment variables."
        )
    
    logger.info(f"[cyan]📤 Uploading file:[/cyan] {file.filename}", extra={"markup": True})
    
    try:
        # Read file content
        content = await file.read()
        
        # Upload to Azure
        public_url = uploader.upload_file(
            file_content=content,
            filename=file.filename,
            content_type=file.content_type
        )
        
        if not public_url:
            raise HTTPException(status_code=500, detail="Failed to upload file to Azure Storage")
        
        logger.info(f"[green]✓ Upload successful:[/green] {file.filename}", extra={"markup": True})
        
        return UploadResponse(
            filename=file.filename,
            public_url=public_url,
            size_bytes=len(content)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[red]Upload error:[/red] {e}", extra={"markup": True})
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/upload_multiple", response_model=MultiUploadResponse)
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files to Azure Blob Storage
    
    Args:
        files: List of files to upload (max 10)
    
    Returns:
        List of public URLs
    """
    if not STORAGE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Azure Storage module not available"
        )
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed")
    
    uploader = get_uploader()
    
    if not uploader.is_configured():
        raise HTTPException(
            status_code=503,
            detail="Azure Storage not configured"
        )
    
    logger.info(f"[cyan]📤 Uploading {len(files)} files[/cyan]", extra={"markup": True})
    
    uploaded_files = []
    
    for file in files:
        try:
            content = await file.read()
            public_url = uploader.upload_file(
                file_content=content,
                filename=file.filename,
                content_type=file.content_type
            )
            
            if public_url:
                uploaded_files.append(UploadResponse(
                    filename=file.filename,
                    public_url=public_url,
                    size_bytes=len(content)
                ))
        except Exception as e:
            logger.error(f"[red]Failed to upload {file.filename}:[/red] {e}", extra={"markup": True})
    
    return MultiUploadResponse(
        files=uploaded_files,
        total_files=len(uploaded_files)
    )


@router.get("/health")
async def storage_health():
    """Check if Azure Storage is configured"""
    if not STORAGE_AVAILABLE:
        return {
            "configured": False,
            "error": "Azure Storage SDK not installed"
        }
    
    uploader = get_uploader()
    return {
        "configured": uploader.is_configured(),
        "container": uploader.container_name if uploader.is_configured() else None
    }
