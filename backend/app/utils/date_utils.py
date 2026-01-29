# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import holidays


def add_months(start_date: date, months: int) -> date:
    """
    Add months to a date, handling month-end edge cases correctly.

    Examples:
        Jan 31 + 1 month = Feb 28/29 (not Mar 2/3)
        Jan 31 + 6 months = Jul 31
    """
    return start_date + relativedelta(months=months)


def is_business_day(target_date: date) -> bool:
    """
    Check if a date is a business day (not weekend or federal holiday).

    Args:
        target_date: Date to check

    Returns:
        True if the date is a business day, False otherwise
    """
    # Check if weekend
    if target_date.weekday() in (5, 6):  # Saturday = 5, Sunday = 6
        return False

    # Check if federal holiday
    us_holidays = holidays.US(years=target_date.year)
    if target_date in us_holidays:
        return False

    return True


def add_business_days(start_date: date, days: int) -> date:
    """
    Add business days to a date, skipping weekends and federal holidays.

    Args:
        start_date: Starting date
        days: Number of business days to add

    Returns:
        Date after adding specified business days
    """
    current_date = start_date
    days_added = 0

    while days_added < days:
        current_date += timedelta(days=1)
        if is_business_day(current_date):
            days_added += 1

    return current_date
