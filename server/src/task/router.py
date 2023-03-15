from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.src.database import get_db
import server.src.category.schemas as schemas
import server.src.category.service as service
import server.src.category.exceptions as exceptions
import server.src.dependencies as glob_dependencies

router = APIRouter(
    prefix="",
    tags=["category"]
)