from datetime import datetime, timedelta
from typing import Tuple

def parse_date(date_str: str) -> datetime:
    """Parse common date formats to a datetime object."""
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str}")

def get_date_range_for_year(year: int) -> Tuple[datetime, datetime]:
    """Get the start and end datetime for a specific year."""
    start_date = datetime(year, 1, 1, 0, 0, 0)
    end_date = datetime(year, 12, 31, 23, 59, 59)
    return start_date, end_date

def get_start_of_month(date: datetime) -> datetime:
    """Return datetime representing the start of the month."""
    return datetime(date.year, date.month, 1)

def format_date_to_str(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """Format datetime to a string."""
    return date.strftime(format_str)
