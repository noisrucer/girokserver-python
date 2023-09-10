from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr

from src.database import get_db
import src.dependencies as glob_dependencies
import src.utils as glob_utils
import src.auth.service as auth_service
import src.auth.exceptions as auth_exceptions
import src.user.schemas as schemas
import src.user.exceptions as exceptions
import src.user.service as service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
