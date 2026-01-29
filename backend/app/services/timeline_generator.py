# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from datetime import date
from ..models.timeline_event import TimelineEvent, EventType, EventStatus
from ..models.leave_request import LeaveRequest
from .deadline_calculator import DeadlineCalculator


class TimelineGenerator:
    """
    Generate timeline events for FMLA leave requests.

    Orchestrates the deadline calculator to create a complete timeline
    of events with appropriate status indicators.
    """

    def __init__(self):
        self.calculator = DeadlineCalculator()

    def generate_timeline(self, leave_request: LeaveRequest) -> list[TimelineEvent]:
        """
        Generate complete timeline for a leave request.

        Args:
            leave_request: The FMLA leave request

        Returns:
            Sorted list of timeline events
        """
        events = []

        # Add leave start event
        events.append(self._create_leave_start_event(leave_request))

        # Add leave end event
        events.append(self._create_leave_end_event(leave_request))

        # Add certification deadline
        cert_deadline_event = self._create_certification_deadline_event(leave_request)
        events.append(cert_deadline_event)

        # Add cure window if certification is missing or incomplete
        if self._needs_cure_window(leave_request):
            cure_events = self._create_cure_window_events(
                cert_deadline_event.event_date
            )
            events.extend(cure_events)

        # Add recertification event
        events.append(self._create_recertification_event(leave_request))

        # Sort events by date
        events.sort(key=lambda e: e.event_date)

        return events

    def _create_leave_start_event(self, leave_request: LeaveRequest) -> TimelineEvent:
        """Create leave start event."""
        event_date = leave_request.leave.start_date
        status = self._calculate_event_status(event_date, completed=False)

        return TimelineEvent(
            event_type=EventType.LEAVE_START,
            event_date=event_date,
            status=status,
            title="Leave Starts",
            description=f"FMLA leave begins for {leave_request.employee.name}",
            is_critical=False
        )

    def _create_leave_end_event(self, leave_request: LeaveRequest) -> TimelineEvent:
        """Create leave end event."""
        event_date = leave_request.leave.end_date
        status = self._calculate_event_status(event_date, completed=False)

        return TimelineEvent(
            event_type=EventType.LEAVE_END,
            event_date=event_date,
            status=status,
            title="Leave Ends",
            description=f"FMLA leave concludes for {leave_request.employee.name}",
            is_critical=False
        )

    def _create_certification_deadline_event(
        self,
        leave_request: LeaveRequest
    ) -> TimelineEvent:
        """Create certification deadline event."""
        notice_date = leave_request.notice_date or date.today()
        event_date = self.calculator.calculate_certification_deadline(
            leave_request.leave.start_date,
            notice_date
        )

        # Check if certification is complete
        completed = (
            leave_request.medical_provider.signature_present and
            leave_request.medical_provider.date_signed is not None
        )

        status = self._calculate_event_status(event_date, completed)

        return TimelineEvent(
            event_type=EventType.CERTIFICATION_DEADLINE,
            event_date=event_date,
            status=status,
            title="Certification Deadline",
            description=(
                "Medical certification must be received by this date. "
                "Employee has 15 calendar days from notice date."
            ),
            is_critical=True
        )

    def _create_cure_window_events(
        self,
        cert_deadline: date
    ) -> list[TimelineEvent]:
        """Create cure window start and end events."""
        cure_start, cure_end = self.calculator.calculate_cure_window(cert_deadline)

        events = []

        # Cure window start
        events.append(TimelineEvent(
            event_type=EventType.CURE_WINDOW_START,
            event_date=cure_start,
            status=self._calculate_event_status(cure_start, completed=False),
            title="Cure Window Begins",
            description=(
                "7-day cure window begins for employee to fix incomplete "
                "or missing documentation."
            ),
            is_critical=True
        ))

        # Cure window end
        events.append(TimelineEvent(
            event_type=EventType.CURE_WINDOW_END,
            event_date=cure_end,
            status=self._calculate_event_status(cure_end, completed=False),
            title="Cure Window Ends",
            description=(
                "Final deadline to provide missing/incomplete documentation. "
                "Leave may be denied if not received."
            ),
            is_critical=True
        ))

        return events

    def _create_recertification_event(
        self,
        leave_request: LeaveRequest
    ) -> TimelineEvent:
        """Create recertification deadline event."""
        event_date = self.calculator.calculate_recertification_date(
            leave_request.leave.start_date,
            leave_request.leave.condition_type.value
        )

        status = self._calculate_event_status(event_date, completed=False)

        condition_label = (
            "6 months" if leave_request.leave.condition_type.value == "chronic"
            else "30 days"
        )

        return TimelineEvent(
            event_type=EventType.RECERTIFICATION_DUE,
            event_date=event_date,
            status=status,
            title="Recertification Due",
            description=(
                f"Medical recertification required ({condition_label} from leave start). "
                "Updated certification must be submitted."
            ),
            is_critical=True
        )

    def _calculate_event_status(
        self,
        event_date: date,
        completed: bool
    ) -> EventStatus:
        """
        Calculate the status of an event based on date and completion.

        Args:
            event_date: Date of the event
            completed: Whether the event has been completed

        Returns:
            EventStatus enum value
        """
        if completed:
            return EventStatus.COMPLETED

        today = date.today()

        if event_date < today:
            return EventStatus.OVERDUE
        elif event_date == today:
            return EventStatus.TODAY
        else:
            return EventStatus.UPCOMING

    def _needs_cure_window(self, leave_request: LeaveRequest) -> bool:
        """
        Determine if cure window events should be added.

        Cure window is needed if:
        - Certification is missing (no signature)
        - Certification is incomplete (compliance flags present)
        - Status is awaiting_docs
        """
        has_signature = leave_request.medical_provider.signature_present
        has_compliance_flags = len(leave_request.compliance_flags) > 0
        is_awaiting_docs = leave_request.status.value == "awaiting_docs"

        return not has_signature or has_compliance_flags or is_awaiting_docs

    def get_at_risk_events(
        self,
        leave_request: LeaveRequest,
        warning_days: int = 3
    ) -> list[TimelineEvent]:
        """
        Get events that are at risk (approaching or overdue).

        Args:
            leave_request: The leave request
            warning_days: Number of days before deadline to consider "approaching"

        Returns:
            List of at-risk events
        """
        timeline = self.generate_timeline(leave_request)
        at_risk = []

        for event in timeline:
            if not event.is_critical:
                continue

            if event.status == EventStatus.OVERDUE:
                at_risk.append(event)
            elif event.status in (EventStatus.UPCOMING, EventStatus.TODAY):
                if self.calculator.is_approaching_deadline(
                    event.event_date,
                    warning_days
                ):
                    at_risk.append(event)

        return at_risk
