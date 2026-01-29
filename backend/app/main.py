# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import leave_requests, timeline, notifications

# Create FastAPI application
app = FastAPI(
    title="FMLA Deadline & Timeline Tracker",
    description="Prototype system for tracking FMLA compliance deadlines and timelines",
    version="0.1.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
