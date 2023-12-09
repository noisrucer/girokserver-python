from datetime import datetime

from pydantic import BaseModel, Field
from src.shared.constants import Priority, RecurrenceType


class CreateEventRequest(BaseModel):
    event_category_path: list | None = Field(
        None,
        description="Event category path the event belongs to. Mutually exclusive with event_id.",
        examples=[["HKU", "COMP3230", "Assignment"]],
    )
    event_category_id: int | None = Field(
        None,
        description="Event category id the event belongs to. Mutually exclusive with event_category_path.",
        examples=[1],
    )
    name: str = Field(..., max_length=300, description="Name of the event", examples=["Appointment with Jason"])
    priority: Priority | None = Field(None, description="Priority of the event", examples=["high"])
    tag: str | None = Field(None, description="Tag of the event", examples=["Work"])
    is_completed: bool = Field(
        False, description="Whether the event is completed or not. Defaults to False.", examples=[False]
    )
    start_date: datetime = Field(..., description="Start date of the event in ISO8601 format")
    end_date: datetime | None = Field(
        None,
        description="End date of the event in ISO8601 format. If provided, it's a one-time event spanning multiple days",  # noqa: E501
    )
    is_recurring: bool = Field(..., description="If true, the event will recur", examples=[False])
    recurrence_type: RecurrenceType | None = Field(
        None, description="Recurrence type of the event, if recurring", examples=["weekly"]
    )
    recurrence_end_date: datetime | None = Field(None, description="If provided, the event will recur until this date")


class Event(BaseModel):
    event_id: int
    user_id: int
    event_category_id: int | None
    name: str
    priority: Priority | None
    tag: str | None
    is_completed: bool
    start_date: datetime
    end_date: datetime | None
    is_recurring: bool
    recurrence_type: RecurrenceType | None
    recurrence_end_date: datetime | None


class GetEventsResponse(BaseModel):
    events: list[Event]
