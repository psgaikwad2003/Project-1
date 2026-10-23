"""Application configuration module using Pydantic Settings for 12-factor compliance."""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Production settings parsed from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "cloudops-nexus"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "production"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = ["*"]

    DATABASE_URL: str = "postgresql://cloudops:cloudops_secret@postgres:5432/cloudops_db"
    REDIS_URL: str = "redis://redis:6379/0"

    METRICS_ENABLED: bool = True
    METRICS_PATH: str = "/metrics"


@lru_cache()
def get_settings() -> Settings:
    """Retrieve cached instance of application settings."""
    return Settings()
