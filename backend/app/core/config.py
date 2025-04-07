from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Interview System"
    
    # Database Settings
    SQLITE_DATABASE_URL: str = "sqlite:///./interview.db"
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_BASE: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    
    # OpenSearch Settings
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 