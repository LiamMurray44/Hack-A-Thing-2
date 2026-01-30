"""
SQLAlchemy ORM models for database tables.

These models define the database schema and are separate from Pydantic models
which handle API validation. The ORM models use JSON columns for embedded objects
(employee, leave, medical_provider) to match the current data structure.

Written by Claude Code on 2026-01-30
User prompt: Database Integration - Add SQLAlchemy with PostgreSQL/MySQL
"""
from sqlalchemy import (
    Column, String, Boolean, Date, DateTime, Text,
    ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, date as date_type

from .database import Base
from ..models.leave_request import LeaveStatus
from ..models.notification import NotificationType
from ..config import settings


# Platform-specific JSON type (JSONB for PostgreSQL, JSON for SQLite)
# Determine based on DATABASE_URL rather than import availability
if settings.DATABASE_URL.startswith('postgresql'):
    from sqlalchemy.dialects.postgresql import JSONB
    JSONType = JSONB
else:
    # Use standard JSON type for SQLite and other databases
    JSONType = JSON


class LeaveRequestDB(Base):
    """
    SQLAlchemy ORM model for leave_requests table.

    Stores FMLA leave requests with embedded JSON objects for employee,
    leave details, and medical provider information.
    """
    __tablename__ = "leave_requests"

    # Primary key
    id = Column(String(50), primary_key=True, index=True)

    # JSON columns (embedded objects)
    # These store complex nested objects as JSON rather than separate tables
    employee = Column(JSONType, nullable=False)
    leave = Column(JSONType, nullable=False)
    medical_provider = Column(JSONType, nullable=False)
    compliance_flags = Column(JSONType, default=list)

    # Scalar columns
    fmla_eligible = Column(Boolean, default=True, nullable=False)
    status = Column(
        SQLEnum(LeaveStatus, native_enum=False, length=20, create_constraint=True),
        nullable=False,
        default=LeaveStatus.PENDING,
        index=True  # Index for filtering by status
    )
    notice_date = Column(Date, nullable=True)
    created_at = Column(Date, nullable=False, default=date_type.today, index=True)

    # Audit timestamp (automatically updated on changes)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationship to notifications
    # cascade="all, delete-orphan" ensures notifications are deleted when request is deleted
    notifications = relationship(
        "NotificationDB",
        back_populates="leave_request",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def to_dict(self) -> dict:
        """
        Convert ORM model to dictionary for Pydantic conversion.

        Returns:
            dict: Dictionary representation matching Pydantic LeaveRequest model
        """
        return {
            "id": self.id,
            "employee": self.employee,
            "leave": self.leave,
            "medical_provider": self.medical_provider,
            "compliance_flags": self.compliance_flags or [],
            "fmla_eligible": self.fmla_eligible,
            "status": self.status.value if isinstance(self.status, LeaveStatus) else self.status,
            "notice_date": self.notice_date.isoformat() if self.notice_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<LeaveRequestDB(id={self.id}, status={self.status}, created_at={self.created_at})>"


class NotificationDB(Base):
    """
    SQLAlchemy ORM model for notifications table.

    Stores email notifications for FMLA events with a foreign key
    relationship to leave requests.
    """
    __tablename__ = "notifications"

    # Primary key
    id = Column(String(50), primary_key=True, index=True)

    # Foreign key to leave_requests
    # ON DELETE CASCADE ensures notifications are deleted when the parent request is deleted
    request_id = Column(
        String(50),
        ForeignKey("leave_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True  # Index for efficient queries by request_id
    )

    # Notification fields
    type = Column(
        SQLEnum(NotificationType, native_enum=False, length=30, create_constraint=True),
        nullable=False,
        index=True  # Index for filtering by type
    )
    recipient = Column(String(255), nullable=False)
    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True  # Index for sorting by creation time
    )
    read_status = Column(Boolean, default=False, nullable=False, index=True)

    # Audit timestamp
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationship to leave request
    leave_request = relationship("LeaveRequestDB", back_populates="notifications")

    def to_dict(self) -> dict:
        """
        Convert ORM model to dictionary for Pydantic conversion.

        Returns:
            dict: Dictionary representation matching Pydantic Notification model
        """
        return {
            "id": self.id,
            "request_id": self.request_id,
            "type": self.type.value if isinstance(self.type, NotificationType) else self.type,
            "recipient": self.recipient,
            "subject": self.subject,
            "body": self.body,
            "created_at": self.created_at.isoformat(),
            "read_status": self.read_status,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<NotificationDB(id={self.id}, type={self.type}, read={self.read_status})>"
