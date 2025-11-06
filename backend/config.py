"""
AI Tanács - Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # Server Config
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000", "*"]

    # Agent Configuration
    max_tokens: int = 500
    temperature: float = 0.7
    timeout_seconds: int = 30

    # Voting Configuration
    voting_method: str = "borda"  # borda, irv, mrr, hybrid

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
