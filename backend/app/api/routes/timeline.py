# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype
# Updated on 2026-01-30: Added database support with dependency injection

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ...models.timeline_event import TimelineEvent
from ...models.compliance import ComplianceStatus
from ...models.leave_request import LeaveRequest
from ...db.database import get_db
from ...storage.storage_factory import get_storage
from ...services.timeline_generator import TimelineGenerator
from ...services.compliance_checker import ComplianceChecker

router = APIRouter(prefix="/api/timeline", tags=["timeline"])
timeline_gen = TimelineGenerator()
compliance_checker = ComplianceChecker()


@router.get("/{request_id}", response_model=list[TimelineEvent])
async def get_timeline(request_id: str, db: Session = Depends(get_db)):
    """
    Get complete timeline for a leave request.

    Returns all timeline events (leave start/end, deadlines, cure window, etc.)
    sorted by date with status indicators.
    """
    storage = get_storage(db)

    # Get the leave request
    request_data = storage.get_leave_request_by_id(request_id)
    if not request_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave request {request_id} not found"
        )

    leave_request = LeaveRequest(**request_data)

    # Generate timeline
    timeline = timeline_gen.generate_timeline(leave_request)

    return timeline


@router.get("/{request_id}/compliance", response_model=ComplianceStatus)
async def get_compliance_status(request_id: str, db: Session = Depends(get_db)):
    """
    Get compliance status for a leave request.

    Returns detailed compliance information including:
    - Whether certification is complete
    - Days until deadline
    - Whether in cure window
    - Risk level
    """
    storage = get_storage(db)

    # Get the leave request
    request_data = storage.get_leave_request_by_id(request_id)
    if not request_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave request {request_id} not found"
        )

    leave_request = LeaveRequest(**request_data)

    # Check compliance
    compliance = compliance_checker.check_compliance(leave_request)

    return compliance


@router.get("/alerts/all", response_model=list[dict])
async def get_all_alerts(db: Session = Depends(get_db)):
    """
    Get all at-risk alerts across all leave requests.

    Returns list of requests with approaching or overdue deadlines,
    sorted by risk level and urgency.
    """
    storage = get_storage(db)

    # Get all leave requests
    requests_data = storage.get_all_leave_requests()
    requests = [LeaveRequest(**data) for data in requests_data]

    # Get at-risk requests
    at_risk = compliance_checker.get_all_at_risk_requests(requests)

    # Format response
    alerts = []
    for request, compliance in at_risk:
        # Get at-risk events from timeline
        at_risk_events = timeline_gen.get_at_risk_events(request)

        alerts.append({
            "request": request.model_dump(mode='json'),
            "compliance": compliance.model_dump(mode='json'),
            "at_risk_events": [e.model_dump(mode='json') for e in at_risk_events]
        })

    return alerts
