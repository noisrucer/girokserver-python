from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String

from src.infrastructure.database.connection import Base
from src.shared.constants import Priority, RecurrenceType


class Event(Base):
    __tablename__ = "event"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    event_category_id = Column(
        Integer, ForeignKey("event_category.event_category_id", ondelete="CASCADE"), nullable=True
    )
    name = Column(String(300), nullable=False)
    priority = Column(Enum(Priority), nullable=True)
    tag = Column(String(20), nullable=True)
    is_completed = Column(Boolean, nullable=False, default=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)  # if provided, it's a one-time event spanning multiple days
    is_recurring = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class EventRecurrence(Base):
    __tablename__ = "event_recurrence"

    recurrence_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("event.event_id"), nullable=False)
    recurrence_type = Column(Enum(RecurrenceType), nullable=False)
    recurrence_end_date = Column(DateTime, nullable=True)
