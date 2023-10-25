from datetime import datetime

from src.shared.constants import Priority, RecurrenceType


class EventEntity:
    def __init__(
        self,
        user_id: int,
        name: str,
        start_date: datetime,
        is_recurring: bool,
        end_date: datetime | None = None,
        event_category_id: int | None = None,
        priority: Priority | None = None,
        tag: str | None = None,
        is_completed: bool = False,
        recurrence_type: RecurrenceType | None = None,
        recurrence_end_date: datetime | None = None,
        event_id: int | None = None,
    ):
        self.user_id = user_id
        self.name = name
        self.start_date = start_date
        self.is_recurring = is_recurring
        self.end_date = end_date
        self.event_category_id = event_category_id
        self.priority = priority
        self.tag = tag
        self.is_completed = is_completed
        self.recurrence_type = recurrence_type
        self.recurrence_end_date = recurrence_end_date
        self.event_id = event_id

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "start_date": self.start_date,
            "is_recurring": self.is_recurring,
            "end_date": self.end_date,
            "event_category_id": self.event_category_id,
            "priority": self.priority,
            "tag": self.tag,
            "is_completed": self.is_completed,
            "recurrence_type": self.recurrence_type,
            "recurrence_end_date": self.recurrence_end_date,
            "event_id": self.event_id,
        }

    def assign_event_id(self, event_id: int) -> None:
        self.event_id = event_id
