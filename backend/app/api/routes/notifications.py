# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from fastapi import APIRouter, HTTPException, status
from typing import Optional
import uuid

from ...models.notification import Notification, NotificationType
from ...models.leave_request import LeaveRequest
from ...storage.json_storage import JSONStorage
from ...services.notification_service import NotificationService

router = APIRouter(prefix="/api/notifications", tags=["notifications"])
storage = JSONStorage()
notification_service = NotificationService()


@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification(
    request_id: str,
    notification_type: NotificationType,
    custom_subject: Optional[str] = None,
    custom_body: Optional[str] = None
):
    """
    Create a new notification for a leave request.

    Can auto-generate notification content based on type, or use custom content.
    """
    # Get the leave request
    request_data = storage.get_leave_request_by_id(request_id)
    if not request_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave request {request_id} not found"
        )

    leave_request = LeaveRequest(**request_data)

    # Generate notification based on type
    if notification_type == NotificationType.CERTIFICATION_DUE:
        from ...services.deadline_calculator import DeadlineCalculator
        calc = DeadlineCalculator()
        cert_deadline = calc.calculate_certification_deadline(
            leave_request.leave.start_date,
            leave_request.notice_date
        )
        notification = notification_service.generate_certification_due_notification(
            leave_request,
            str(cert_deadline)
        )

    elif notification_type == NotificationType.CURE_WINDOW:
        from ...services.deadline_calculator import DeadlineCalculator
        calc = DeadlineCalculator()
        cert_deadline = calc.calculate_certification_deadline(
            leave_request.leave.start_date,
            leave_request.notice_date
        )
        _, cure_end = calc.calculate_cure_window(cert_deadline)
        notification = notification_service.generate_cure_window_notification(
            leave_request,
            str(cure_end),
            leave_request.compliance_flags
        )

    elif notification_type == NotificationType.RECERTIFICATION_DUE:
        from ...services.deadline_calculator import DeadlineCalculator
        calc = DeadlineCalculator()
        recert_date = calc.calculate_recertification_date(
            leave_request.leave.start_date,
            leave_request.leave.condition_type.value
        )
        notification = notification_service.generate_recertification_notification(
            leave_request,
            str(recert_date)
        )

    elif notification_type == NotificationType.APPROVAL_NOTICE:
        notification = notification_service.generate_approval_notification(leave_request)

    elif notification_type == NotificationType.DENIAL_NOTICE:
        reason = "Incomplete or missing medical certification"
        notification = notification_service.generate_denial_notification(
            leave_request,
            reason
        )

    elif notification_type == NotificationType.MISSING_DOCS:
        notification = notification_service.generate_missing_docs_notification(
            leave_request,
            leave_request.compliance_flags
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown notification type: {notification_type}"
        )

    # Override with custom content if provided
    if custom_subject:
        notification.subject = custom_subject
    if custom_body:
        notification.body = custom_body

    # Store notification
    notification_dict = notification.model_dump(mode='json')
    storage.create_notification(notification_dict)

    return notification


@router.get("/{request_id}", response_model=list[Notification])
async def get_notifications_for_request(request_id: str):
    """
    Get all notifications for a specific leave request.
    """
    # Verify request exists
    request_data = storage.get_leave_request_by_id(request_id)
    if not request_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave request {request_id} not found"
        )

    # Get notifications
    notifications_data = storage.get_notifications_by_request_id(request_id)
    notifications = [Notification(**data) for data in notifications_data]

    # Sort by created_at (newest first)
    notifications.sort(key=lambda n: n.created_at, reverse=True)

    return notifications


@router.get("/", response_model=list[Notification])
async def get_all_notifications(
    notification_type: Optional[NotificationType] = None,
    unread_only: bool = False
):
    """
    Get all notifications with optional filtering.

    Query parameters:
    - notification_type: Filter by type
    - unread_only: Only return unread notifications
    """
    notifications_data = storage.get_all_notifications()
    notifications = [Notification(**data) for data in notifications_data]

    # Apply filters
    if notification_type:
        notifications = [n for n in notifications if n.type == notification_type]

    if unread_only:
        notifications = [n for n in notifications if not n.read_status]

    # Sort by created_at (newest first)
    notifications.sort(key=lambda n: n.created_at, reverse=True)

    return notifications


@router.patch("/{notification_id}", response_model=Notification)
async def update_notification(notification_id: str, read_status: bool):
    """
    Update notification read status.
    """
    if read_status:
        updated = storage.mark_notification_as_read(notification_id)
    else:
        updated = storage.mark_notification_as_unread(notification_id)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification {notification_id} not found"
        )

    return Notification(**updated)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(notification_id: str):
    """
    Delete a notification.
    """
    success = storage.delete_notification(notification_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification {notification_id} not found"
        )

    return None
