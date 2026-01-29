# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from datetime import date
from ..models.compliance import ComplianceStatus
from ..models.leave_request import LeaveRequest
from .deadline_calculator import DeadlineCalculator


class ComplianceChecker:
    """
    Check FMLA compliance status for leave requests.
    """

    def __init__(self):
        self.calculator = DeadlineCalculator()

    def check_compliance(self, leave_request: LeaveRequest) -> ComplianceStatus:
        """
        Check compliance status for a leave request.

        Args:
            leave_request: The leave request to check

        Returns:
            ComplianceStatus with detailed compliance information
        """
        notice_date = leave_request.notice_date or date.today()
        cert_deadline = self.calculator.calculate_certification_deadline(
            leave_request.leave.start_date,
            notice_date
        )

        # Check if certification is received and complete
        cert_received = leave_request.medical_provider.signature_present
        cert_complete = (
            cert_received and
            len(leave_request.compliance_flags) == 0
        )

        # Calculate days until deadline
        days_until_deadline = self.calculator.calculate_days_until(cert_deadline)

        # Check if in cure window
        today = date.today()
        in_cure_window = False
        cure_window_end = None

        if not cert_complete and today > cert_deadline:
            # Past certification deadline without complete docs = in cure window
            cure_start, cure_end = self.calculator.calculate_cure_window(cert_deadline)
            if cure_start <= today <= cure_end:
                in_cure_window = True
                cure_window_end = cure_end

        # Determine if compliant
        is_compliant = cert_complete and days_until_deadline >= 0

        # Calculate risk level
        at_risk, risk_level = self._calculate_risk_level(
            days_until_deadline,
            cert_received,
            cert_complete,
            in_cure_window
        )

        return ComplianceStatus(
            request_id=leave_request.id,
            is_compliant=is_compliant,
            certification_received=cert_received,
            certification_complete=cert_complete,
            certification_deadline=cert_deadline,
            days_until_certification_deadline=days_until_deadline,
            in_cure_window=in_cure_window,
            cure_window_end=cure_window_end,
            compliance_issues=leave_request.compliance_flags,
            at_risk=at_risk,
            risk_level=risk_level
        )

    def _calculate_risk_level(
        self,
        days_until_deadline: int,
        cert_received: bool,
        cert_complete: bool,
        in_cure_window: bool
    ) -> tuple[bool, str]:
        """
        Calculate risk level based on deadline proximity and certification status.

        Returns:
            Tuple of (at_risk: bool, risk_level: str)
            Risk levels: "none", "low", "medium", "high"
        """
        # High risk: overdue or in cure window
        if days_until_deadline < 0 or in_cure_window:
            return (True, "high")

        # Medium risk: deadline within 3 days and incomplete
        if days_until_deadline <= 3 and not cert_complete:
            return (True, "medium")

        # Low risk: deadline within 7 days and incomplete
        if days_until_deadline <= 7 and not cert_complete:
            return (True, "low")

        # No risk: either complete or deadline is far away
        return (False, "none")

    def get_all_at_risk_requests(
        self,
        leave_requests: list[LeaveRequest]
    ) -> list[tuple[LeaveRequest, ComplianceStatus]]:
        """
        Get all leave requests that are at risk.

        Args:
            leave_requests: List of leave requests to check

        Returns:
            List of tuples (leave_request, compliance_status) for at-risk requests
        """
        at_risk = []

        for request in leave_requests:
            compliance = self.check_compliance(request)
            if compliance.at_risk:
                at_risk.append((request, compliance))

        # Sort by risk level (high to low) then by days until deadline
        risk_order = {"high": 0, "medium": 1, "low": 2, "none": 3}
        at_risk.sort(
            key=lambda x: (
                risk_order[x[1].risk_level],
                x[1].days_until_certification_deadline
            )
        )

        return at_risk
