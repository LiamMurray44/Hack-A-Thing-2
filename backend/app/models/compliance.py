# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from pydantic import BaseModel, Field
from datetime import date


class ComplianceStatus(BaseModel):
    """
    Compliance status for an FMLA leave request.
    """

    request_id: str = Field(..., description="Associated leave request ID")
    is_compliant: bool = Field(..., description="Whether request is fully compliant")
    certification_received: bool = Field(
        ...,
        description="Whether medical certification has been received"
    )
    certification_complete: bool = Field(
        ...,
        description="Whether certification is complete (no missing info)"
    )
    certification_deadline: date = Field(
        ...,
        description="Deadline for certification submission"
    )
    days_until_certification_deadline: int = Field(
        ...,
        description="Days until certification deadline (negative if overdue)"
    )
    in_cure_window: bool = Field(
        default=False,
        description="Whether currently in 7-day cure window"
    )
    cure_window_end: date | None = Field(
        None,
        description="End date of cure window (if applicable)"
    )
    compliance_issues: list[str] = Field(
        default_factory=list,
        description="List of compliance issues/flags"
    )
    at_risk: bool = Field(
        default=False,
        description="Whether any deadlines are approaching or overdue"
    )
    risk_level: str = Field(
        default="none",
        description="Risk level: none, low, medium, high"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req-123",
                "is_compliant": False,
                "certification_received": True,
                "certification_complete": False,
                "certification_deadline": "2025-02-16",
                "days_until_certification_deadline": 3,
                "in_cure_window": False,
                "cure_window_end": None,
                "compliance_issues": ["missing_physician_phone"],
                "at_risk": True,
                "risk_level": "medium"
            }
        }
