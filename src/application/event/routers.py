from fastapi import APIRouter, Depends, status

from src.application.event.dtos import CreateEventRequest
from src.dependencies.auth_dependencies import get_current_user_id
from src.dependencies.event_dependencies import get_event_service
from src.domain.event.services import EventService

router = APIRouter(prefix="/events", tags=["event"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(
    request: CreateEventRequest,
    event_service: EventService = Depends(get_event_service),
    current_user_id: str = Depends(get_current_user_id),
):
    pass
