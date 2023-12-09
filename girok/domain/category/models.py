from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from girok.core.db.session_maker import Base


class Category(AsyncAttrs, Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"), nullable=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    children: Mapped[list["Category"]] = relationship(
        "Category", back_populates="parent", cascade="all, delete-orphan", lazy="selectin"
    )
    parent: Mapped["Category"] = relationship("Category", back_populates="children", remote_side=[id])
