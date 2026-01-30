"""
Application configuration using Pydantic Settings.

Written by Claude Code on 2026-01-30
User prompt: Database Integration - Add SQLAlchemy with PostgreSQL/MySQL
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables can be defined in a .env file or set in the system.
    """

    # Database configuration
    DATABASE_URL: str = "sqlite:///./data/fmla_tracker.db"

    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production
    DEBUG: bool = True

    # API Configuration
    API_TITLE: str = "FMLA Deadline & Timeline Tracker"
    API_VERSION: str = "0.2.0"
    API_DESCRIPTION: str = """
    Prototype system for tracking FMLA compliance deadlines and timelines.

    **Version 0.2.0** introduces database persistence:
    - SQLite for development (no server setup required)
    - PostgreSQL support for production
    - Improved query performance with indexes
    - Data integrity with foreign keys
    - Transaction support with ACID guarantees
    - Feature flag for safe rollback to JSON storage

    All API endpoints remain backward compatible.
    """

    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    # Feature flags
    USE_DATABASE: bool = True  # Toggle between database and JSON file storage

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra environment variables
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses lru_cache to ensure settings are only loaded once and reused.

    Returns:
        Settings instance with configuration values
    """
    return Settings()


# Global settings instance
settings = get_settings()
