from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import Boolean

from src.infrastructure.database.connection import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_verified = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class EmailVerification(Base):
    __tablename__ = "email_verification"

    email_verification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    verification_code = Column(String(6), nullable=False)
    expiration_time = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(minutes=1))
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())


class EmailVerificationCode(Base):
    __tablename__ = "email_verification_code"

    email_verification_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False, unique=True)
    verification_code = Column(String(6), nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    expiration_time = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(minutes=1))
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
