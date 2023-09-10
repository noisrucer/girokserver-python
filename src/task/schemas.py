from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, DateTime
from typing import Union, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime

import src.auth.exceptions as auth_exceptions

class TaskCreateIn(BaseModel):
    task_category_id: Union[int, None] = None
    name: str
    deadline: str
    priority: int = Field(default=None, ge=1, le=5)
    color: Union[str, None] = None
    everyday: Union[bool, None] = False
    tag: Union[str, None] = None
    is_time: bool = False
    all_day: Union[bool, None] = False
    weekly_repeat: int = Field(default=None, gt=0, le=6)


class TaskCreateOut(BaseModel):
    task_id: int
    
    class Config:
        orm_mode = True
        

class Task(BaseModel):
    task_id: int
    user_id: int
    task_category_id: Union[int, None]
    category_path: Union[str, None]
    name: str
    color: str
    deadline: str
    all_day: Union[bool, None]
    is_time: bool
    priority: Union[int, None]
    everyday: Union[bool, None]
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class GetSingleTaskOut(BaseModel):
    name: str
    
        
class TaskOut(BaseModel):
    tasks: Dict[str, dict]
    
    
class Tag(BaseModel):
    tag_id: int
    task_id: int
    name: int
    
class TagOut(BaseModel):
    tags: List[str]
    

class ChangeTaskTagIn(BaseModel):
    new_tag_name: str


class ChangeTaskPriorityIn(BaseModel):
    new_priority: int = Field(ge=1, le=5)


class ChangeTaskDateIn(BaseModel):
    new_date: str = Field(default=..., regex="^([0-9]){4}-([0-9]){1,2}-([0-9]){1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}$")


class ChangeTaskNameIn(BaseModel):
    new_name: str