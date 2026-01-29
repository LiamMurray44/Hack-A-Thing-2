# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from pydantic import BaseModel, Field, field_validator
from datetime import date
from enum import Enum
from .employee import Employee


class LeaveStatus(str, Enum):
    """Status of an FMLA leave request."""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    AWAITING_DOCS = "awaiting_docs"


class ConditionType(str, Enum):
    """Type of medical condition for recertification timing."""
    SERIOUS = "serious"
    CHRONIC = "chronic"


class Leave(BaseModel):
    """Leave details for FMLA request."""

    start_date: date = Field(..., description="Leave start date")
    end_date: date = Field(..., description="Leave end date")
    intermittent: bool = Field(default=False, description="Whether leave is intermittent")
    condition_type: ConditionType = Field(
        default=ConditionType.SERIOUS,
        description="Type of medical condition"
    )

    @field_validator("end_date")
    @classmethod
    def validate_end_after_start(cls, v: date, info) -> date:
        """Validate that end date is after start date."""
        if "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("Leave end date must be after start date")
        return v


class MedicalProvider(BaseModel):
    """Medical provider information."""

    name: str = Field(..., description="Provider name")
    phone: str | None = Field(None, description="Provider phone number")
    signature_present: bool = Field(
        default=False,
        description="Whether provider signature is present"
    )
    date_signed: date | None = Field(None, description="Date certification was signed")


class LeaveRequestCreate(BaseModel):
    """Model for creating a new FMLA leave request (without ID)."""

    employee: Employee = Field(..., description="Employee information")
    leave: Leave = Field(..., description="Leave details")
    medical_provider: MedicalProvider = Field(..., description="Medical provider information")
    compliance_flags: list[str] = Field(
        default_factory=list,
        description="List of compliance issues (e.g., 'missing_physician_phone')"
    )
    status: LeaveStatus = Field(
        default=LeaveStatus.PENDING,
        description="Current status of the request"
    )
    notice_date: date | None = Field(
        None,
        description="Date employee gave notice of leave (defaults to today)"
    )


class LeaveRequest(BaseModel):
    """Complete FMLA leave request."""

    id: str = Field(..., description="Unique identifier for the request")
    employee: Employee = Field(..., description="Employee information")
    leave: Leave = Field(..., description="Leave details")
    medical_provider: MedicalProvider = Field(..., description="Medical provider information")
    compliance_flags: list[str] = Field(
        default_factory=list,
        description="List of compliance issues (e.g., 'missing_physician_phone')"
    )
    status: LeaveStatus = Field(
        default=LeaveStatus.PENDING,
        description="Current status of the request"
    )
    notice_date: date | None = Field(
        None,
        description="Date employee gave notice of leave (defaults to today)"
    )
    created_at: date = Field(
        default_factory=date.today,
        description="Date request was created"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "req-123",
                "employee": {
                    "name": "Jane Doe",
                    "ssn_last4": "1234",
                    "phone": "(555) 555-5555",
                    "email": "jane.doe@example.com"
                },
                "leave": {
                    "start_date": "2025-02-01",
                    "end_date": "2025-04-01",
                    "intermittent": False,
                    "condition_type": "serious"
                },
                "medical_provider": {
                    "name": "Dr. John Smith",
                    "signature_present": True,
                    "date_signed": "2025-01-20"
                },
                "compliance_flags": ["missing_physician_phone"],
                "status": "pending"
            }
        }
