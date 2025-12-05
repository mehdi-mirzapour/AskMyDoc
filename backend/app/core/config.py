from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application settings - reads from backend/.env file"""
    
    # API Keys - reads from OPENAI_API_KEY in .env file
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    mistral_api_key: str = "XXXX"
    
    # Langfuse Configuration
    langfuse_public_key: str = Field(default="XXXX", alias="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: str = Field(default="XXXX", alias="LANGFUSE_SECRET_KEY")
    langfuse_host: str = Field(default="https://cloud.langfuse.com", alias="LANGFUSE_BASE_URL")
    
    # Model Configuration - using OpenAI with gpt-4o-mini
    active_model: str = "openai"  # Options: "openai" or "mistral"
    
    # Application Settings
    upload_dir: str = "uploads"
    max_file_size_mb: int = 50
    
    class Config:
        # Look for .env file in the backend directory
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
