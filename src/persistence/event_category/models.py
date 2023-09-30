from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.infrastructure.database.connection import Base


class EventCategory(Base):
    __tablename__ = "event_category"
    event_category_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    name = Column(String(50), nullable=False)
    parent_event_category_id = Column(Integer, ForeignKey("event_category.event_category_id"), nullable=True)
    color = Column(String(7), nullable=False)
    children = relationship("EventCategory", back_populates="parent", remote_side=[event_category_id])
    parent = relationship("EventCategory", back_populates="children", cascade="all, delete-orphan")
