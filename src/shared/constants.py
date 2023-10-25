from enum import Enum

DEFAULT_CATEGORY_COLOR = "#FFE7A0"


class Priority(Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RecurrenceType(Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"
