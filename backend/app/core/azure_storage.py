"""
Azure Blob Storage utility for uploading files
"""
try:
    from azure.storage.blob import BlobServiceClient, PublicAccess, ContentSettings
    AZURE_STORAGE_AVAILABLE = True
except ImportError:
    AZURE_STORAGE_AVAILABLE = False
    BlobServiceClient = None
    PublicAccess = None
    ContentSettings = None

from pathlib import Path
import os
from typing import Optional
from app.core.logger import logger
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class AzureStorageUploader:
    """Handle file uploads to Azure Blob Storage"""
    
    def __init__(self):
        """Initialize Azure Blob Storage client"""
        # Check if Azure Storage SDK is available
        if not AZURE_STORAGE_AVAILABLE:
            logger.warning("[yellow]Azure Storage SDK not installed - storage endpoints disabled[/yellow]", extra={"markup": True})
            self.blob_service_client = None
            self.container_name = "excel-files"
            return
        
        # Get configuration from environment
        self.storage_account = os.getenv("AZURE_STORAGE_ACCOUNT")
        self.storage_key = os.getenv("AZURE_STORAGE_KEY")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER", "excel-files")
        
        # Check if credentials are configured
        if not self.storage_account or not self.storage_key:
            logger.warning("[yellow]Azure Storage credentials not configured[/yellow]", extra={"markup": True})
            self.blob_service_client = None
            return
        
        # Create connection string
        connection_string = (
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={self.storage_account};"
            f"AccountKey={self.storage_key};"
            f"EndpointSuffix=core.windows.net"
        )
        
        # Initialize client
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            self._ensure_container_exists()
            logger.info(f"[green]✓ Azure Storage initialized:[/green] {self.container_name}", extra={"markup": True})
        except Exception as e:
            logger.error(f"[red]Failed to initialize Azure Storage:[/red] {e}", extra={"markup": True})
            self.blob_service_client = None
    
    def _ensure_container_exists(self):
        """Create container with public blob access if it doesn't exist"""
        if not self.blob_service_client:
            return
        
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            
            # Try to get container properties - will raise if doesn't exist
            try:
                container_client.get_container_properties()
                logger.info(f"[green]✓ Container exists:[/green] {self.container_name}", extra={"markup": True})
            except Exception:
                # Container doesn't exist, create it
                container_client = self.blob_service_client.create_container(
                    self.container_name,
                    public_access=PublicAccess.Blob  # Public read access
                )
                logger.info(f"[green]✓ Created container:[/green] {self.container_name}", extra={"markup": True})
                
        except Exception as e:
            logger.error(f"[red]Error with container:[/red] {e}", extra={"markup": True})
    
    def upload_file(self, file_content: bytes, filename: str, content_type: Optional[str] = None) -> Optional[str]:
        """Upload file to Azure Blob Storage
        
        Args:
            file_content: File content as bytes
            filename: Name for the blob
            content_type: MIME type (optional)
        
        Returns:
            Public URL of uploaded file, or None if failed
        """
        if not self.blob_service_client:
            logger.error("[red]Azure Storage not configured[/red]", extra={"markup": True})
            return None
        
        try:
            # Ensure container exists before upload
            try:
                container_client = self.blob_service_client.get_container_client(self.container_name)
                container_client.get_container_properties()
            except Exception:
                # Create container if it doesn't exist
                logger.info(f"[yellow]Creating container:[/yellow] {self.container_name}", extra={"markup": True})
                self.blob_service_client.create_container(
                    self.container_name,
                    public_access=PublicAccess.Blob
                )
                logger.info(f"[green]✓ Container created[/green]", extra={"markup": True})
            
            # Upload blob
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=filename
            )
            
            # Set content type if provided
            content_settings = None
            if content_type:
                content_settings = ContentSettings(content_type=content_type)
            
            # Upload
            blob_client.upload_blob(
                file_content,
                overwrite=True,
                content_settings=content_settings
            )
            
            # Return public URL
            public_url = blob_client.url
            logger.info(f"[green]✓ Uploaded to Azure:[/green] {filename}", extra={"markup": True})
            return public_url
            
        except Exception as e:
            logger.error(f"[red]Upload failed:[/red] {e}", extra={"markup": True})
            return None
    
    def is_configured(self) -> bool:
        """Check if Azure Storage is properly configured"""
        return self.blob_service_client is not None


# Global instance
_uploader = None

def get_uploader() -> AzureStorageUploader:
    """Get or create Azure Storage uploader instance"""
    global _uploader
    if _uploader is None:
        _uploader = AzureStorageUploader()
    return _uploader
