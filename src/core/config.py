from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # LLM Settings
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    
    # Database Settings
    DATABASE_URL: str
    REDIS_URL: str
    
    # Optional Settings
    LOG_LEVEL: str = "INFO"
    MAX_BATCH_SIZE: int = 100
    CACHE_TTL: int = 3600
    
    # Language Processing
    SPACY_MODEL: str = "en_core_web_sm"
    TRANSLATION_API_KEY: Optional[str] = None
    
    # Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10_485_760  # 10MB in bytes
    
    # Security
    API_KEY_HEADER: str = "X-API-Key"
    RATE_LIMIT: int = 100
    
    # Output settings
    SAVE_RESULTS: bool = True
    OUTPUT_DIR: str = "output"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 