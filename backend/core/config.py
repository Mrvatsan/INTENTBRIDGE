"""
Configuration module for IntentBridge.

Loads environment variables from .env and provides application-wide settings
through a Pydantic BaseSettings instance. All settings can be overridden via
environment variables or the .env file.
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "IntentBridge"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    GOOGLE_API_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    USE_MOCK_AI: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
