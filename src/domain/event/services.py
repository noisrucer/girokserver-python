from datetime import datetime

from src.persistence.event.repositories import EventRepository


class EventService:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def create_event(
        self,
        name: str,
        priority: str,
        tag: str,
        status: str,
        start_date: datetime,
        end_date: datetime,
        is_recurring: bool,
        recurrence_type: str,
        recurrence_end_date: datetime,
        user_id: str,
        event_category_id: str,
    ):
        pass
        # if end_date is provided, is_recurring must be False
        # if is_recurring is True, end_date must be None
        # if is_recurring is True, then recurrence_type must be provided (and optionally recurrence_end_date)
        # if is_recurring is False, then recurrence_type must be None and also recurrence_end_date must be None
        # if request.is_recurring

        # if is_recurring is True, then recurrence_type must be provided
