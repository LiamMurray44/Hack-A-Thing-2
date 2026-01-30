"""
Storage factory for selecting JSON or database storage.

This module provides a factory function to return the appropriate storage
implementation based on configuration. This allows for easy A/B testing and
graceful rollback between database and JSON file storage.

Written by Claude Code on 2026-01-30
User prompt: Database Integration - Add SQLAlchemy with PostgreSQL/MySQL
"""
from sqlalchemy.orm import Session
from ..config import settings
from .json_storage import JSONStorage
from .db_storage import DBStorage


def get_storage(db: Session = None):
    """
    Get storage implementation based on configuration.

    The storage implementation is selected based on the USE_DATABASE setting
    in the application configuration (.env file). This enables:
    - Seamless switching between database and JSON storage
    - Safe rollback in case of database issues
    - A/B testing of performance

    Args:
        db: Database session (required if USE_DATABASE=True)

    Returns:
        Storage implementation (JSONStorage or DBStorage)

    Raises:
        ValueError: If USE_DATABASE=True but no database session provided

    Example:
        # In a FastAPI route with database dependency
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            storage = get_storage(db)
            items = storage.get_all_leave_requests()
            return items

        # For JSON storage (when USE_DATABASE=False in .env)
        storage = get_storage()
        items = storage.get_all_leave_requests()
    """
    if settings.USE_DATABASE:
        if db is None:
            raise ValueError(
                "Database session required when USE_DATABASE=True. "
                "Ensure db parameter is provided (e.g., db: Session = Depends(get_db))"
            )
        return DBStorage(db)
    else:
        # JSON storage doesn't need database session
        return JSONStorage()
