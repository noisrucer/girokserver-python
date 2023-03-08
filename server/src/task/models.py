from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from server.src.database import Base


class Task(Base):
    __tablename__ = "task"
    
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    task_category_id = Column(Integer, ForeignKey('task_category.task_category_id'), nullable=True)
    name = Column(String(300), nullable=False)
    deadline = Column(DateTime, nullable=False)
    priority = Column(Integer, nullable=True)
    color = Column(String(20), nullable=True)
    recurring = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
