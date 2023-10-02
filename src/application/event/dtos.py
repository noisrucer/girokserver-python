from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Priority(Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Status(Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    done = "done"


class RecurrenceType(Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class CreateEventRequest(BaseModel):
    name: str = Field(..., max_length=300, description="Name of the event", examples=["Appointment with Jason"])
    priority: Priority | None = Field(None, description="Priority of the event", examples=["high"])
    tag: str | None = Field(None, description="Tag of the event", examples=["Work"])
    status: Status | None = Field(
        None, description="Status of the event. It must be one of 'not_started', 'in_progress', 'done'.", examples=[]
    )
    start_date: datetime = Field(..., description="Start date of the event in ISO8601 format")
    end_date: datetime | None = Field(None, description="If provided, it's a one-time event spanning multiple days")
    is_recurring: bool = Field(..., description="If true, the event will recur", examples=[True])
    recurrence_type: RecurrenceType | None = Field(
        None, description="Recurrence type of the event, if recurring", examples=["weekly"]
    )
    recurrence_end_date: datetime | None = Field(None, description="If provided, the event will recur until this date")
