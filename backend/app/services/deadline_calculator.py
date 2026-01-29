# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from datetime import date, timedelta
from ..utils.date_utils import add_months, is_business_day


class DeadlineCalculator:
    """
    Core FMLA deadline calculation logic.

    All deadlines use CALENDAR DAYS unless explicitly noted.
    This is the most critical component for FMLA compliance.
    """

    @staticmethod
    def calculate_certification_deadline(
        leave_start_date: date,
        notice_date: date | None = None
    ) -> date:
        """
        Calculate the deadline for employee to provide medical certification.

        FMLA Rule: Employee has 15 calendar days from when notice is given,
        BUT certification must be received by the time leave begins.

        Args:
            leave_start_date: Date when leave begins
            notice_date: Date when employee gave notice (defaults to today)

        Returns:
            Certification deadline date (earlier of 15 days after notice OR leave start)

        Examples:
            Leave starts Feb 15, notice given Feb 1 → Deadline = Feb 16 (15 days after notice)
            Leave starts Feb 1, notice given Jan 25 → Deadline = Feb 1 (leave start)
        """
        if notice_date is None:
            notice_date = date.today()

        # 15 calendar days from notice
        fifteen_day_deadline = notice_date + timedelta(days=15)

        # Certification must be received by leave start date
        # Return the earlier of the two dates
        return min(fifteen_day_deadline, leave_start_date)

    @staticmethod
    def calculate_cure_window(certification_deadline: date) -> tuple[date, date]:
        """
        Calculate the 7-day cure window for fixing incomplete documentation.

        FMLA Rule: If certification is incomplete/insufficient, employer must
        provide written notice and employee has 7 calendar days to cure deficiencies.

        Args:
            certification_deadline: The original certification deadline

        Returns:
            Tuple of (cure_start_date, cure_end_date)

        Example:
            Certification deadline Feb 16 → Cure window = Feb 17 to Feb 23
        """
        # Cure window starts the day after certification deadline
        cure_start = certification_deadline + timedelta(days=1)

        # Cure window is 7 calendar days
        cure_end = certification_deadline + timedelta(days=7)

        return (cure_start, cure_end)

    @staticmethod
    def calculate_recertification_date(
        leave_start_date: date,
        condition_type: str = "serious"
    ) -> date:
        """
        Calculate when recertification is required.

        FMLA Rules:
        - Serious health condition: Minimum 30 days
        - Chronic condition: Every 6 months
        - Can also be as specified by medical provider (not implemented in prototype)

        Args:
            leave_start_date: Date when leave begins
            condition_type: "serious" or "chronic"

        Returns:
            Date when recertification is due

        Examples:
            Leave starts Feb 1, serious condition → Recert = Mar 3 (30 days)
            Leave starts Feb 1, chronic condition → Recert = Aug 1 (6 months)
        """
        if condition_type == "chronic":
            # 6 months for chronic conditions
            return add_months(leave_start_date, 6)
        else:
            # 30 calendar days minimum for serious health conditions
            return leave_start_date + timedelta(days=30)

    @staticmethod
    def is_approaching_deadline(deadline_date: date, warning_days: int = 3) -> bool:
        """
        Check if a deadline is approaching (within specified warning days).

        Args:
            deadline_date: The deadline to check
            warning_days: Number of days before deadline to trigger warning (default 3)

        Returns:
            True if deadline is within warning_days of today
        """
        today = date.today()
        days_until = (deadline_date - today).days
        return 0 <= days_until <= warning_days

    @staticmethod
    def is_overdue(deadline_date: date) -> bool:
        """
        Check if a deadline has passed.

        Args:
            deadline_date: The deadline to check

        Returns:
            True if deadline is in the past
        """
        return deadline_date < date.today()

    @staticmethod
    def calculate_days_until(target_date: date) -> int:
        """
        Calculate number of days until a target date.

        Args:
            target_date: The target date

        Returns:
            Number of days (negative if in the past)
        """
        return (target_date - date.today()).days
