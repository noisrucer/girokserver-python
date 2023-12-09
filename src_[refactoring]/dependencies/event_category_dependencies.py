from fastapi import Depends
from sqlalchemy.orm import Session
from src.domain.event_category.services import EventCategoryService
from src.infrastructure.database.session import get_db
from src.persistence.event_category.repositories import EventCategoryRepository


def get_event_category_service(session: Session = Depends(get_db)) -> EventCategoryService:
    repository = EventCategoryRepository(session=session)
    return EventCategoryService(event_category_repository=repository)
