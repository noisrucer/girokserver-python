from datetime import datetime

from src.domain.event.entities import EventEntity
from src.domain.event.exceptions import InvalidEventError
from src.persistence.event.repositories import EventRepository


class EventService:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def create_event(
        self,
        user_id: str,
        name: str,
        start_date: datetime,
        is_recurring: bool,
        end_date: datetime | None = None,
        event_category_id: str | None = None,
        priority: str | None = None,
        tag: str | None = None,
        is_completed: bool = False,
        recurrence_type: str | None = None,
        recurrence_end_date: datetime | None = None,
    ):
        if end_date and is_recurring:
            raise InvalidEventError(detail="If end_date is provided, is_recurring must be False")
        if is_recurring and not recurrence_type:
            raise InvalidEventError(detail="If an event is recurring, then recurrence_type must be provided")
        if not is_recurring and (recurrence_type or recurrence_end_date):
            raise InvalidEventError(
                detail="If an event is not recurring, then recurrence_type and recurrence_end_date must not be provided"
            )
        event_entity = EventEntity(
            user_id=user_id,
            name=name,
            start_date=start_date,
            is_recurring=is_recurring,
            end_date=end_date,
            event_category_id=event_category_id,
            priority=priority,
            tag=tag,
            is_completed=is_completed,
            recurrence_type=recurrence_type,
            recurrence_end_date=recurrence_end_date,
        )
        self.event_repository.create_event(event_entity)

    def get_all_events(
        self,
        start_date: datetime,
        end_date: datetime,
        no_category: bool | None = None,
        event_category_id: int | None = None,
        priority: str | None = None,
        tag: str | None = None,
    ) -> list[EventEntity]:
        return self.event_repository.get_all_events(
            start_date=start_date,
            end_date=end_date,
            no_category=no_category,
            event_category_id=event_category_id,
            priority=priority,
            tag=tag,
        )
