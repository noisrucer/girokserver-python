from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from sqlalchemy.sql.expression import text

from server.src.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_token"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), unique=True)
    refresh_token = Column(String(500), nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))