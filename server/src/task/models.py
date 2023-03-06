from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from server.src.database import Base


class Task(Base):
    __tablename__ = "task"
    
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(100), ForeignKey("user.email"), nullable=False)
    task_category_id = Column(Integer, ForeignKey('task_category.task_category_id'), nullable=True)
    title = Column(String(300), nullable=False)
    deadline = Column(DateTime, nullable=False)
    importance = Column(Integer, nullable=True)
    color = Column(String(20), nullable=True)
