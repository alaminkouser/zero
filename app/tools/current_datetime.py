from datetime import datetime


def current_datetime() -> datetime:
    """
    Returns the current local date and time as an ISO 8601 datetime string.
    """
    return datetime.now()
