from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, DateTime
from typing import Union, List, Dict
from email_validator import validate_email,  EmailNotValidError
from pydantic import BaseModel, validator, Field
from datetime import datetime

import server.src.auth.exceptions as auth_exceptions

class TaskCreateIn(BaseModel):
    task_category_id: Union[int, None] = None
    name: str
    deadline: str
    priority: int = Field(default=None, gt=1, le=5)
    color: Union[str, None] = None
    recurring: Union[int, None] = None

class TaskCreateOut(BaseModel):
    task_id: int
    
    class Config:
        orm_mode = True
        
        
class TaskOut(BaseModel):
    test: int
    