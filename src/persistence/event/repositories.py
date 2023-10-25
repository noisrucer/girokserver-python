from datetime import datetime, timedelta

from sqlalchemy import and_, extract, func, or_
from sqlalchemy.orm import Session

from src.domain.event.entities import EventEntity
from src.persistence.event.models import Event, EventRecurrence
from src.shared.constants import RecurrenceType


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_event(self, event_entity: EventEntity) -> None:
        event = Event(
            user_id=event_entity.user_id,
            event_category_id=event_entity.event_category_id,
            name=event_entity.name,
            priority=event_entity.priority,
            tag=event_entity.tag,
            is_completed=event_entity.is_completed,
            start_date=event_entity.start_date,
            end_date=event_entity.end_date,
            is_recurring=event_entity.is_recurring,
        )
        self.session.add(event)
        self.session.commit()
        event_entity.assign_event_id(event.event_id)

        if event.is_recurring:
            event_recurrence = EventRecurrence(
                event_id=event.event_id,
                recurrence_type=event_entity.recurrence_type,
                recurrence_end_date=event_entity.recurrence_end_date,
            )
            self.session.add(event_recurrence)
            self.session.commit()

    def get_all_events(
        self,
        start_date: datetime,
        end_date: datetime,
        no_category: bool | None = None,
        event_category_id: int | None = None,
        priority: str | None = None,
        tag: str | None = None,
    ) -> list[EventEntity]:
        non_recurring_query = self.session.query(Event).filter(
            or_(
                Event.start_date.between(start_date, end_date),
                Event.end_date.between(start_date, end_date),
                (Event.start_date <= start_date) & (Event.end_date >= end_date),
            )
        )

        # Recurring events query
        recurring_conditions = [
            Event.is_recurring is True,
            Event.start_date <= end_date,
            or_(EventRecurrence.recurrence_end_date is None, EventRecurrence.recurrence_end_date >= start_date),
            or_(
                EventRecurrence.recurrence_type == RecurrenceType.daily,
                and_(
                    EventRecurrence.recurrence_type == RecurrenceType.weekly,
                    func.floor((extract("day", end_date - Event.start_date) % 7) + func.DAYOFWEEK(Event.start_date))
                    >= func.DAYOFWEEK(start_date),
                    func.floor((extract("day", end_date - Event.start_date) % 7) + func.DAYOFWEEK(Event.start_date))
                    <= func.DAYOFWEEK(end_date),
                ),
                and_(
                    EventRecurrence.recurrence_type == RecurrenceType.monthly,
                    or_(
                        extract("day", Event.start_date).between(extract("day", start_date), extract("day", end_date)),
                        and_(
                            extract("day", Event.start_date) > extract("day", start_date + timedelta(days=-1)),
                            extract("day", start_date) == extract("day", start_date + timedelta(days=-1)),
                        ),
                        and_(
                            extract("day", Event.start_date) > extract("day", end_date + timedelta(days=-1)),
                            extract("day", end_date) == extract("day", end_date + timedelta(days=-1)),
                        ),
                    ),
                ),
            ),
        ]

        recurring_query = (
            self.session.query(Event)
            .join(EventRecurrence, Event.event_id == EventRecurrence.event_id)
            .filter(*recurring_conditions)
        )

        # Combine and execute both queries
        query = non_recurring_query.union_all(recurring_query).order_by(Event.start_date)

        if no_category:
            query = query.filter(Event.event_category_id is None)
        elif event_category_id:
            query = query.filter(Event.event_category_id == event_category_id)
        if priority:
            query = query.filter(Event.priority == priority)
        if tag:
            query = query.filter(Event.tag == tag)

        events = query.all()
        event_entities = []
        for event in events:
            event_entity = EventEntity(
                user_id=event.user_id,
                name=event.name,
                start_date=event.start_date,
                is_recurring=event.is_recurring,
                end_date=event.end_date,
                event_category_id=event.event_category_id,
                priority=event.priority,
                tag=event.tag,
                is_completed=event.is_completed,
                event_id=event.event_id,
            )
            if event.is_recurring:
                event_recurrence = (
                    self.session.query(EventRecurrence).filter(EventRecurrence.event_id == event.event_id).first()
                )
                event_entity.recurrence_type = event_recurrence.recurrence_type
                event_entity.recurrence_end_date = event_recurrence.recurrence_end_date

            event_entities.append(event_entity)

        return event_entities
