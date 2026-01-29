# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    """Types of email notifications."""
    CERTIFICATION_DUE = "certification_due"
    CURE_WINDOW = "cure_window"
    RECERTIFICATION_DUE = "recertification_due"
    APPROVAL_NOTICE = "approval_notice"
    DENIAL_NOTICE = "denial_notice"
    MISSING_DOCS = "missing_docs"


class Notification(BaseModel):
    """
    Email notification for FMLA events.

    In this prototype, notifications are displayed in the UI
    rather than actually sent via email.
    """

    id: str = Field(..., description="Unique notification identifier")
    request_id: str = Field(..., description="Associated leave request ID")
    type: NotificationType = Field(..., description="Type of notification")
    recipient: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When notification was created"
    )
    read_status: bool = Field(default=False, description="Whether notification has been read")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "notif-123",
                "request_id": "req-456",
                "type": "certification_due",
                "recipient": "jane.doe@example.com",
                "subject": "FMLA Certification Due in 3 Days",
                "body": "Your medical certification is due by February 16, 2025...",
                "created_at": "2025-02-13T10:00:00",
                "read_status": False
            }
        }
