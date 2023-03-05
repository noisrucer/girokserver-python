from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr

from server.src.database import get_db
import server.src.dependencies as glob_dependencies
import server.src.utils as glob_utils
import server.src.auth.service as auth_service
import server.src.auth.exceptions as auth_exceptions
import server.src.user.schemas as schemas
import server.src.user.exceptions as exceptions
import server.src.user.service as service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
