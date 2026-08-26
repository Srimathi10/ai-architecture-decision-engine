from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Architecture Decision Engine"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/arch_engine"
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    class Config:
        env_file = ".env"

settings = Settings()
