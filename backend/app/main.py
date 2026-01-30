# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype
# Updated on 2026-01-30: Added database support with configuration management

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import leave_requests, timeline, notifications
from .config import settings
from .db.database import init_db

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event: Initialize database
@app.on_event("startup")
async def startup_event():
    """
    Initialize database on application startup.

    Creates all tables if they don't exist.
    Only runs if USE_DATABASE=true in configuration.
    """
    if settings.USE_DATABASE:
        init_db()
        print(f"Database initialized: {settings.DATABASE_URL}")
    else:
        print("Using JSON file storage (USE_DATABASE=false)")

# Include routers
app.include_router(leave_requests.router)
app.include_router(timeline.router)
app.include_router(notifications.router)


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "name": "FMLA Deadline & Timeline Tracker API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
