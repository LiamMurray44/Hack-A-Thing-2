# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class EventType(str, Enum):
    """Types of timeline events."""
    LEAVE_START = "leave_start"
    LEAVE_END = "leave_end"
    CERTIFICATION_DEADLINE = "certification_deadline"
    CURE_WINDOW_START = "cure_window_start"
    CURE_WINDOW_END = "cure_window_end"
    RECERTIFICATION_DUE = "recertification_due"


class EventStatus(str, Enum):
    """Status of a timeline event."""
    UPCOMING = "upcoming"
    TODAY = "today"
    OVERDUE = "overdue"
    COMPLETED = "completed"


class TimelineEvent(BaseModel):
    """A single event on the FMLA timeline."""

    event_type: EventType = Field(..., description="Type of event")
    event_date: date = Field(..., description="Date of the event")
    status: EventStatus = Field(..., description="Current status of the event")
    title: str = Field(..., description="Display title for the event")
    description: str = Field(..., description="Detailed description of the event")
    is_critical: bool = Field(
        default=False,
        description="Whether this is a critical compliance deadline"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "certification_deadline",
                "event_date": "2025-02-16",
                "status": "upcoming",
                "title": "Certification Deadline",
                "description": "Medical certification must be received by this date",
                "is_critical": True
            }
        }
