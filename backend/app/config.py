from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lenny Growth Assistant"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password123@localhost:5432/lenny_assistant"
    
    # LLM Settings
    DEFAULT_LLM_PROVIDER: str = "claude"  # or "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"
    
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Vector Search Settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    SIMILARITY_THRESHOLD: float = 0.5
    TOP_K_CHUNKS: int = 5

    class Config:
        env_file = "../.env"

settings = Settings()
