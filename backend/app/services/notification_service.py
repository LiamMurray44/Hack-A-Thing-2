# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import uuid
from datetime import datetime
from ..models.notification import Notification, NotificationType
from ..models.leave_request import LeaveRequest
from .deadline_calculator import DeadlineCalculator


class NotificationService:
    """
    Generate and manage FMLA email notifications.

    In this prototype, notifications are stored and displayed in the UI
    rather than actually sent via email.
    """

    def __init__(self):
        self.calculator = DeadlineCalculator()

    def generate_certification_due_notification(
        self,
        leave_request: LeaveRequest,
        cert_deadline: str
    ) -> Notification:
        """
        Generate notification for upcoming certification deadline.

        Sent 3 days before deadline.
        """
        recipient = leave_request.employee.email or f"{leave_request.employee.ssn_last4}@example.com"

        subject = "FMLA Certification Due in 3 Days"
        body = f"""Dear {leave_request.employee.name},

This is a reminder that your FMLA medical certification is due by {cert_deadline}.

Please ensure that your healthcare provider completes and submits the medical certification form by this deadline. The certification must include:
- Your medical condition details
- Expected duration of leave
- Healthcare provider's signature and contact information

If you have any questions, please contact HR.

Best regards,
FMLA Compliance Team"""

        return Notification(
            id=str(uuid.uuid4()),
            request_id=leave_request.id,
            type=NotificationType.CERTIFICATION_DUE,
            recipient=recipient,
            subject=subject,
            body=body
        )

    def generate_cure_window_notification(
        self,
        leave_request: LeaveRequest,
        cure_end_date: str,
        missing_items: list[str]
    ) -> Notification:
        """
        Generate notification for cure window opening.

        Sent when certification is incomplete/missing.
        """
        recipient = leave_request.employee.email or f"{leave_request.employee.ssn_last4}@example.com"

        missing_items_text = "\n".join([f"- {item}" for item in missing_items])

        subject = "Action Required: 7-Day Cure Window for FMLA Certification"
        body = f"""Dear {leave_request.employee.name},

Your FMLA medical certification has been reviewed and is incomplete or missing required information.

You have 7 calendar days (until {cure_end_date}) to provide the following:

{missing_items_text}

This is your final opportunity to submit complete documentation. If the required information is not received by {cure_end_date}, your FMLA leave request may be denied.

Please contact HR immediately if you have questions.

Best regards,
FMLA Compliance Team"""

        return Notification(
            id=str(uuid.uuid4()),
            request_id=leave_request.id,
            type=NotificationType.CURE_WINDOW,
            recipient=recipient,
            subject=subject,
            body=body
        )

    def generate_recertification_notification(
        self,
        leave_request: LeaveRequest,
        recert_date: str
    ) -> Notification:
        """
        Generate notification for recertification requirement.

        Sent 7 days before recertification due date.
        """
        recipient = leave_request.employee.email or f"{leave_request.employee.ssn_last4}@example.com"

        subject = "FMLA Recertification Required"
        body = f"""Dear {leave_request.employee.name},

Your FMLA leave that began on {leave_request.leave.start_date} requires medical recertification.

A new medical certification form must be submitted by {recert_date}.

Please have your healthcare provider complete an updated certification that includes:
- Current status of your medical condition
- Expected continued duration of leave
- Any changes to treatment or prognosis

Contact HR if you need a new certification form or have questions.

Best regards,
FMLA Compliance Team"""

        return Notification(
            id=str(uuid.uuid4()),
            request_id=leave_request.id,
            type=NotificationType.RECERTIFICATION_DUE,
            recipient=recipient,
            subject=subject,
            body=body
        )

    def generate_approval_notification(
        self,
        leave_request: LeaveRequest
    ) -> Notification:
        """
        Generate notification for leave approval.
        """
        recipient = leave_request.employee.email or f"{leave_request.employee.ssn_last4}@example.com"

        subject = "FMLA Leave Request Approved"
        body = f"""Dear {leave_request.employee.name},

Your FMLA leave request has been approved.

Leave Details:
- Start Date: {leave_request.leave.start_date}
- End Date: {leave_request.leave.end_date}
- Type: {"Intermittent" if leave_request.leave.intermittent else "Continuous"}

Important Reminders:
- Keep HR informed of any changes to your leave dates
- Submit recertification if required
- Contact HR before returning to work

If you have questions about your leave, please contact HR.

Best regards,
FMLA Compliance Team"""

        return Notification(
            id=str(uuid.uuid4()),
            request_id=leave_request.id,
            type=NotificationType.APPROVAL_NOTICE,
            recipient=recipient,
            subject=subject,
            body=body
        )

    def generate_denial_notification(
        self,
        leave_request: LeaveRequest,
        reason: str
    ) -> Notification:
        """
        Generate notification for leave denial.
        """
        recipient = leave_request.employee.email or f"{leave_request.employee.ssn_last4}@example.com"

        subject = "FMLA Leave Request Denied"
        body = f"""Dear {leave_request.employee.name},

Your FMLA leave request has been denied.

Reason: {reason}

If you believe this decision was made in error or have additional documentation to support your request, please contact HR within 5 business days.

You have the right to:
- Request clarification of this decision
- Provide additional medical documentation
- File an appeal

Please contact HR for more information about your options.

Best regards,
FMLA Compliance Team"""

        return Notification(
            id=str(uuid.uuid4()),
            request_id=leave_request.id,
            type=NotificationType.DENIAL_NOTICE,
            recipient=recipient,
            subject=subject,
            body=body
        )

    def generate_missing_docs_notification(
        self,
        leave_request: LeaveRequest,
        missing_items: list[str]
    ) -> Notification:
        """
        Generate notification for missing documentation.
        """
        recipient = leave_request.employee.email or f"{leave_request.employee.ssn_last4}@example.com"

        missing_items_text = "\n".join([f"- {item}" for item in missing_items])

        subject = "Missing Documentation for FMLA Leave Request"
        body = f"""Dear {leave_request.employee.name},

Your FMLA leave request is missing required documentation.

Please provide the following as soon as possible:

{missing_items_text}

Your leave request cannot be processed until all required documentation is received.

Contact HR if you need assistance obtaining these documents.

Best regards,
FMLA Compliance Team"""

        return Notification(
            id=str(uuid.uuid4()),
            request_id=leave_request.id,
            type=NotificationType.MISSING_DOCS,
            recipient=recipient,
            subject=subject,
            body=body
        )
