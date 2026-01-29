# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from fastapi import APIRouter, HTTPException, status
from typing import Optional
import uuid
from datetime import date

from ...models.leave_request import LeaveRequest, LeaveRequestCreate, LeaveStatus
from ...storage.json_storage import JSONStorage

router = APIRouter(prefix="/api/leave-requests", tags=["leave-requests"])
storage = JSONStorage()


@router.post("/", response_model=LeaveRequest, status_code=status.HTTP_201_CREATED)
async def create_leave_request(request: LeaveRequestCreate):
    """
    Create a new FMLA leave request.

    Accepts JSON with employee, leave, and medical provider information.
    """
    # Generate ID
    request_id = f"req-{uuid.uuid4().hex[:8]}"

    # Set notice date to today if not provided
    notice_date = request.notice_date or date.today()

    # Create full leave request with ID
    full_request = LeaveRequest(
        id=request_id,
        employee=request.employee,
        leave=request.leave,
        medical_provider=request.medical_provider,
        compliance_flags=request.compliance_flags,
        status=request.status,
        notice_date=notice_date,
        created_at=date.today()
    )

    # Convert to dict for storage
    request_dict = full_request.model_dump(mode='json')

    # Store in JSON file
    storage.create_leave_request(request_dict)

    return full_request


@router.get("/", response_model=list[LeaveRequest])
async def get_all_leave_requests(
    status_filter: Optional[LeaveStatus] = None,
    at_risk_only: bool = False
):
    """
    Get all leave requests with optional filtering.

    Query parameters:
    - status_filter: Filter by status (pending, approved, denied, awaiting_docs)
    - at_risk_only: Only return requests with approaching/overdue deadlines
    """
    requests_data = storage.get_all_leave_requests()
    requests = [LeaveRequest(**data) for data in requests_data]

    # Apply status filter
    if status_filter:
        requests = [r for r in requests if r.status == status_filter]

    # Apply at-risk filter
    if at_risk_only:
        from ...services.compliance_checker import ComplianceChecker
        checker = ComplianceChecker()
        requests = [
            r for r in requests
            if checker.check_compliance(r).at_risk
        ]

    return requests


@router.get("/{request_id}", response_model=LeaveRequest)
async def get_leave_request(request_id: str):
    """
    Get a specific leave request by ID.
    """
    request_data = storage.get_leave_request_by_id(request_id)

    if not request_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave request {request_id} not found"
        )

    return LeaveRequest(**request_data)


@router.patch("/{request_id}", response_model=LeaveRequest)
async def update_leave_request(request_id: str, updates: dict):
    """
    Update a leave request.

    Can update status, compliance flags, or other fields.
    """
    # Verify request exists
    existing = storage.get_leave_request_by_id(request_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave request {request_id} not found"
        )

    # Update the request
    updated = storage.update_leave_request(request_id, updates)

    return LeaveRequest(**updated)


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_leave_request(request_id: str):
    """
    Delete a leave request.
    """
    success = storage.delete_leave_request(request_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave request {request_id} not found"
        )

    return None
