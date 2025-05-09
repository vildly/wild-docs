from pydantic_settings import BaseSettings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Docs Agent API"
    PROJECT_URL: str = "http://localhost:3000"  # Required for OpenRouter
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Qdrant Settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "docs-agent"
    
    # OpenRouter Settings
    OPENROUTER_API_KEY: str
    DEFAULT_MODEL: str = "anthropic/claude-3-haiku"
    
    # OpenAI Settings (for embeddings)
    OPENAI_API_KEY: str
    
    # Document Processing
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: set = {"pdf", "docx", "md"}
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
logger.info(f"OpenRouter API Key loaded: {'Yes' if settings.OPENROUTER_API_KEY else 'No'}")
logger.info(f"OpenAI API Key loaded: {'Yes' if settings.OPENAI_API_KEY else 'No'}")
