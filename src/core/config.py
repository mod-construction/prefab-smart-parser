from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # LLM Settings
    OPENAI_API_KEY: str = ""
    
    # Database Settings
    DATABASE_URL: str = ""
    REDIS_URL: str = ""

    class Config:
        env_file = ".env"

settings = Settings() 