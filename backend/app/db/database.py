"""
Database configuration and session management.

This module provides:
- SQLAlchemy engine creation (SQLite for dev, PostgreSQL for prod)
- Session factory for database operations
- Base declarative class for ORM models
- Dependency injection for FastAPI routes

Written by Claude Code on 2026-01-30
User prompt: Database Integration - Add SQLAlchemy with PostgreSQL/MySQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..config import settings


# Create database engine based on DATABASE_URL
if settings.DATABASE_URL.startswith('sqlite'):
    # SQLite configuration (development)
    # Use StaticPool for single connection and disable same thread check
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},  # Allow multi-threaded access
        poolclass=StaticPool,  # Single connection for SQLite
        echo=settings.DEBUG,  # Log SQL statements in debug mode
    )
else:
    # PostgreSQL configuration (production)
    # Use connection pooling for better performance and concurrency
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using them
        pool_size=10,  # Number of connections in the pool
        max_overflow=20,  # Additional connections beyond pool_size
        echo=settings.DEBUG,  # Log SQL statements in debug mode
    )


# Session factory
# Configured with autocommit=False to require explicit commits
# autoflush=False prevents automatic SQL execution before queries
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Declarative base for ORM models
# All database models should inherit from this Base class
Base = declarative_base()


def get_db():
    """
    Dependency injection for database sessions in FastAPI routes.

    Usage in route functions:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            # Use db session here
            ...

    The session is automatically created at the start of the request
    and closed at the end, ensuring proper cleanup.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.

    This function should be called on application startup.
    It creates all tables defined by SQLAlchemy ORM models
    that inherit from Base.

    Note: In production, use Alembic migrations instead of
    calling this function directly.
    """
    # Import all ORM models to ensure they are registered with Base
    from .models import LeaveRequestDB, NotificationDB  # noqa: F401

    # Create all tables
    Base.metadata.create_all(bind=engine)
