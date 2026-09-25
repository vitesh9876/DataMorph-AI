import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "DataMorph AI API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./datamorph.db"

    # Directories
    UPLOAD_DIR: str = str(BASE_DIR / "storage" / "uploads")
    EXPORT_DIR: str = str(BASE_DIR / "storage" / "exports")
    CACHE_DIR: str = str(BASE_DIR / "storage" / "cache")

    # LLM Settings
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    MAX_ROWS_ANALYSIS: int = 5000

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
for folder in [settings.UPLOAD_DIR, settings.EXPORT_DIR, settings.CACHE_DIR]:
    os.makedirs(folder, exist_ok=True)
