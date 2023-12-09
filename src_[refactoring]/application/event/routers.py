from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from src.application.event.dtos import CreateEventRequest, Event
from src.application.event.exceptions import InvalidEventError
from src.dependencies.auth_dependencies import get_current_user_id
from src.dependencies.event_category_dependencies import get_event_category_service
from src.dependencies.event_dependencies import get_event_service
from src.domain.event.services import EventService
from src.domain.event_category.services import EventCategoryService
from src.shared.constants import Priority

router = APIRouter(prefix="/events", tags=["event"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(
    request: CreateEventRequest,
    event_service: EventService = Depends(get_event_service),
    event_category_service: EventCategoryService = Depends(get_event_category_service),
    current_user_id: str = Depends(get_current_user_id),
):
    if request.event_category_path and request.event_category_id:
        raise InvalidEventError("event_category_path and event_category_id are mutually exclusive")

    # Get event category id from event category path
    cid = None
    if request.event_category_path or request.event_category_id:
        cid = (
            request.event_category_id
            if request.event_category_id
            else event_category_service._get_last_cid_from_path(request.event_category_path, current_user_id)
        )

    event_service.create_event(
        user_id=current_user_id,
        name=request.name,
        start_date=request.start_date,
        is_recurring=request.is_recurring,
        end_date=request.end_date,
        event_category_id=cid,
        priority=request.priority,
        tag=request.tag,
        is_completed=request.is_completed,
        recurrence_type=request.recurrence_type,
        recurrence_end_date=request.recurrence_end_date,
    )


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_events(
    no_category: Annotated[
        bool | None,
        Query(
            description="If true, only return events without a category.\nIf true, then you must not provide event_category_path or event_category_id",  # noqa: E501
            examples=[True],
        ),
    ] = None,
    event_category_path: Annotated[
        list[str] | None,
        Query(
            description="Event category path the event belongs to. Mutually exclusive with event_id.",
            examples=[["HKU", "COMP3230", "Assignment"]],
        ),
    ] = None,
    event_category_id: Annotated[
        int | None,
        Query(
            description="Event category id the event belongs to. Mutually exclusive with event_category_path.",
            examples=[1],
        ),
    ] = None,
    start_date: Annotated[
        datetime,
        Query(
            description="Start date of the event in ISO8601 format",
            examples=["2021-09-01T00:00:00"],
        ),
    ] = datetime(2000, 1, 1),
    end_date: Annotated[
        datetime,
        Query(
            description="End date of the event in ISO8601 format",
            examples=["2021-09-30T00:00:00"],
        ),
    ] = datetime.now()
    + timedelta(days=365 * 10),
    priority: Annotated[
        Priority | None, Query(description="Priority of the event. One of 'low', 'medium', 'high'.", examples=["high"])
    ] = None,
    tag: Annotated[str | None, Query(description="Tag of the event.", examples=["Work"])] = None,
    event_service: EventService = Depends(get_event_service),
    event_category_service: EventCategoryService = Depends(get_event_category_service),
    current_user_id: str = Depends(get_current_user_id),
):
    if no_category and (event_category_path or event_category_id):
        raise InvalidEventError("no_category and event_category_path/event_category_id are mutually exclusive")
    if event_category_path and event_category_id:
        raise InvalidEventError("event_category_path and event_category_id are mutually exclusive")

    cid = None
    if event_category_path or event_category_id:
        cid = (
            event_category_id
            if event_category_id
            else event_category_service._get_last_cid_from_path(event_category_path, current_user_id)
        )

    event_entities = event_service.get_all_events(
        start_date=start_date,
        end_date=end_date,
        no_category=no_category,
        event_category_id=cid,
        priority=priority,
        tag=tag,
    )
    res = []
    for event_entity in event_entities:
        res.append(
            Event(
                event_id=event_entity.event_id,
                user_id=event_entity.user_id,
                event_category_id=event_entity.event_category_id,
                name=event_entity.name,
                priority=event_entity.priority,
                tag=event_entity.tag,
                is_completed=event_entity.is_completed,
                start_date=event_entity.start_date,
                end_date=event_entity.end_date,
                is_recurring=event_entity.is_recurring,
                recurrence_type=event_entity.recurrence_type,
                recurrence_end_date=event_entity.recurrence_end_date,
            )
        )

    return {"events": res}
