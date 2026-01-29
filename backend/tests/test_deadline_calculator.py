# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import pytest
from datetime import date, timedelta
from app.services.deadline_calculator import DeadlineCalculator


class TestCertificationDeadline:
    """Test certification deadline calculations."""

    def test_basic_certification_deadline(self):
        """
        Leave starts Feb 20, notice given Feb 1
        Expected: Deadline = Feb 16 (15 days after notice)
        """
        leave_start = date(2025, 2, 20)
        notice = date(2025, 2, 1)

        deadline = DeadlineCalculator.calculate_certification_deadline(
            leave_start, notice
        )

        assert deadline == date(2025, 2, 16)

    def test_certification_deadline_capped_at_leave_start(self):
        """
        Leave starts Feb 1, notice given Jan 25
        Expected: Deadline = Feb 1 (not Feb 9)
        Certification must be received by leave start date.
        """
        leave_start = date(2025, 2, 1)
        notice = date(2025, 1, 25)

        deadline = DeadlineCalculator.calculate_certification_deadline(
            leave_start, notice
        )

        # 15 days from Jan 25 would be Feb 9, but deadline is capped at leave start
        assert deadline == date(2025, 2, 1)

    def test_certification_deadline_defaults_to_today(self):
        """
        If no notice date provided, should default to today.
        """
        leave_start = date.today() + timedelta(days=30)

        deadline = DeadlineCalculator.calculate_certification_deadline(leave_start)

        expected = date.today() + timedelta(days=15)
        assert deadline == expected

    def test_certification_same_day_notice_and_leave(self):
        """
        If notice and leave start on same day, deadline = same day.
        """
        leave_start = date(2025, 3, 1)
        notice = date(2025, 3, 1)

        deadline = DeadlineCalculator.calculate_certification_deadline(
            leave_start, notice
        )

        assert deadline == date(2025, 3, 1)


class TestCureWindow:
    """Test cure window calculations."""

    def test_cure_window_calculation(self):
        """
        Certification deadline Feb 16
        Expected: Cure window = Feb 17 to Feb 23
        """
        cert_deadline = date(2025, 2, 16)

        cure_start, cure_end = DeadlineCalculator.calculate_cure_window(cert_deadline)

        assert cure_start == date(2025, 2, 17)
        assert cure_end == date(2025, 2, 23)

    def test_cure_window_is_seven_days(self):
        """
        Cure window should always be exactly 7 calendar days.
        """
        cert_deadline = date(2025, 1, 15)

        cure_start, cure_end = DeadlineCalculator.calculate_cure_window(cert_deadline)

        delta = (cure_end - cure_start).days
        assert delta == 6  # Feb 17 to Feb 23 is 6 days difference (inclusive = 7 days)

    def test_cure_window_month_boundary(self):
        """
        Test cure window crossing month boundary.
        """
        cert_deadline = date(2025, 1, 28)

        cure_start, cure_end = DeadlineCalculator.calculate_cure_window(cert_deadline)

        assert cure_start == date(2025, 1, 29)
        assert cure_end == date(2025, 2, 4)


class TestRecertification:
    """Test recertification date calculations."""

    def test_thirty_day_recertification_serious_condition(self):
        """
        Leave starts Feb 1 (serious condition)
        Expected: Recert = Mar 3
        """
        leave_start = date(2025, 2, 1)

        recert_date = DeadlineCalculator.calculate_recertification_date(
            leave_start, "serious"
        )

        assert recert_date == date(2025, 3, 3)

    def test_six_month_recertification_chronic_condition(self):
        """
        Leave starts Feb 1 (chronic condition)
        Expected: Recert = Aug 1
        """
        leave_start = date(2025, 2, 1)

        recert_date = DeadlineCalculator.calculate_recertification_date(
            leave_start, "chronic"
        )

        assert recert_date == date(2025, 8, 1)

    def test_recertification_month_end_edge_case(self):
        """
        Leave starts Jan 31, add 6 months (chronic)
        Expected: Jul 31 (not Aug 2 or Aug 3)
        """
        leave_start = date(2025, 1, 31)

        recert_date = DeadlineCalculator.calculate_recertification_date(
            leave_start, "chronic"
        )

        assert recert_date == date(2025, 7, 31)

    def test_recertification_february_edge_case(self):
        """
        Leave starts Aug 31, add 6 months
        Expected: Feb 28/29 (depending on leap year)
        """
        # Non-leap year
        leave_start = date(2025, 8, 31)
        recert_date = DeadlineCalculator.calculate_recertification_date(
            leave_start, "chronic"
        )
        assert recert_date == date(2026, 2, 28)

        # Leap year
        leave_start = date(2024, 8, 31)
        recert_date = DeadlineCalculator.calculate_recertification_date(
            leave_start, "chronic"
        )
        assert recert_date == date(2025, 2, 28)

    def test_recertification_defaults_to_serious(self):
        """
        If condition type not specified, should default to 30 days.
        """
        leave_start = date(2025, 3, 1)

        recert_date = DeadlineCalculator.calculate_recertification_date(leave_start)

        assert recert_date == date(2025, 3, 31)


class TestDeadlineStatus:
    """Test deadline status checking methods."""

    def test_is_approaching_deadline_within_warning(self):
        """Test deadline approaching detection."""
        # Deadline in 2 days (within 3-day warning)
        deadline = date.today() + timedelta(days=2)
        assert DeadlineCalculator.is_approaching_deadline(deadline, warning_days=3)

    def test_is_approaching_deadline_exactly_on_warning(self):
        """Test deadline exactly at warning threshold."""
        deadline = date.today() + timedelta(days=3)
        assert DeadlineCalculator.is_approaching_deadline(deadline, warning_days=3)

    def test_is_not_approaching_deadline_too_far(self):
        """Test deadline too far in future."""
        deadline = date.today() + timedelta(days=5)
        assert not DeadlineCalculator.is_approaching_deadline(deadline, warning_days=3)

    def test_is_overdue_past_deadline(self):
        """Test overdue detection for past deadline."""
        deadline = date.today() - timedelta(days=1)
        assert DeadlineCalculator.is_overdue(deadline)

    def test_is_not_overdue_today(self):
        """Test that today is not overdue."""
        deadline = date.today()
        assert not DeadlineCalculator.is_overdue(deadline)

    def test_is_not_overdue_future(self):
        """Test that future deadline is not overdue."""
        deadline = date.today() + timedelta(days=1)
        assert not DeadlineCalculator.is_overdue(deadline)

    def test_calculate_days_until_future(self):
        """Test days until calculation for future date."""
        target = date.today() + timedelta(days=5)
        assert DeadlineCalculator.calculate_days_until(target) == 5

    def test_calculate_days_until_past(self):
        """Test days until calculation for past date (negative)."""
        target = date.today() - timedelta(days=3)
        assert DeadlineCalculator.calculate_days_until(target) == -3

    def test_calculate_days_until_today(self):
        """Test days until calculation for today."""
        target = date.today()
        assert DeadlineCalculator.calculate_days_until(target) == 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_leap_year_handling(self):
        """Test that leap year dates are handled correctly."""
        # Feb 29, 2024 (leap year)
        leave_start = date(2024, 2, 29)
        notice = date(2024, 2, 20)

        deadline = DeadlineCalculator.calculate_certification_deadline(
            leave_start, notice
        )

        # 15 days from Feb 20 is Mar 6
        assert deadline == leave_start  # Capped at Feb 29

    def test_year_boundary(self):
        """Test calculations crossing year boundary."""
        leave_start = date(2025, 1, 5)
        notice = date(2024, 12, 25)

        deadline = DeadlineCalculator.calculate_certification_deadline(
            leave_start, notice
        )

        # 15 days from Dec 25, 2024 is Jan 9, 2025
        # But capped at leave start
        assert deadline == date(2025, 1, 5)

    def test_weekend_deadline_not_adjusted(self):
        """
        FMLA deadlines use CALENDAR DAYS.
        Weekend deadlines should NOT be auto-adjusted to business days.
        """
        # Leave starts on Monday Feb 17, 2025
        leave_start = date(2025, 2, 20)
        # Notice given on Saturday Feb 1
        notice = date(2025, 2, 1)

        deadline = DeadlineCalculator.calculate_certification_deadline(
            leave_start, notice
        )

        # Should be Sunday Feb 16 (15 days later), not adjusted to Monday
        assert deadline == date(2025, 2, 16)
        # Verify it's actually a Sunday (weekday 6)
        assert deadline.weekday() == 6  # 6 = Sunday
