# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from pydantic import BaseModel, Field, field_validator
import re


class Employee(BaseModel):
    """Employee information for FMLA leave request."""

    name: str = Field(..., min_length=1, description="Employee full name")
    ssn_last4: str = Field(..., description="Last 4 digits of SSN")
    phone: str = Field(..., description="Employee phone number")
    email: str | None = Field(None, description="Employee email address")
    state: str | None = Field(None, description="Employee state/location")

    @field_validator("ssn_last4")
    @classmethod
    def validate_ssn_last4(cls, v: str) -> str:
        """Validate SSN last 4 digits are exactly 4 digits."""
        if not re.match(r"^\d{4}$", v):
            raise ValueError("SSN last 4 must be exactly 4 digits")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number format."""
        # Remove common formatting characters
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(r"^\d{10}$", cleaned):
            raise ValueError("Phone number must contain 10 digits")
        return v
