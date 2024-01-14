from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.event.services import EventService
from src.infrastructure.database.session import get_db
from src.persistence.event.repositories import EventRepository


def get_event_service(session: Session = Depends(get_db)) -> EventService:
    event_repository = EventRepository(session=session)
    return EventService(event_repository=event_repository)
