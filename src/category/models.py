from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class TaskCategory(Base):
    __tablename__ = "task_category"
    task_category_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    name = Column(String(50), nullable=False)
    super_task_category_id = Column(Integer, ForeignKey("task_category.task_category_id"), nullable=True)
    color = Column(String(20), nullable=True)
    children = relationship("TaskCategory", cascade="all,delete")
