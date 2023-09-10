from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreateIn(BaseModel):
    task_category_id: int | None = None
    name: str
    deadline: str
    priority: int = Field(default=None, ge=1, le=5)
    color: str | None = None
    everyday: bool | None = False
    tag: str | None = None
    is_time: bool = False
    all_day: bool | None = False
    weekly_repeat: int = Field(default=None, gt=0, le=6)


class TaskCreateOut(BaseModel):
    task_id: int

    class Config:
        orm_mode = True


class Task(BaseModel):
    task_id: int
    user_id: int
    task_category_id: int | None
    category_path: str | None
    name: str
    color: str
    deadline: str
    all_day: bool | None
    is_time: bool
    priority: int | None
    everyday: bool | None
    created_at: datetime

    class Config:
        orm_mode = True


class GetSingleTaskOut(BaseModel):
    name: str


class TaskOut(BaseModel):
    tasks: dict[str, dict]


class Tag(BaseModel):
    tag_id: int
    task_id: int
    name: int


class TagOut(BaseModel):
    tags: list[str]


class ChangeTaskTagIn(BaseModel):
    new_tag_name: str


class ChangeTaskPriorityIn(BaseModel):
    new_priority: int = Field(ge=1, le=5)


class ChangeTaskDateIn(BaseModel):
    new_date: str = Field(default=..., regex="^([0-9]){4}-([0-9]){1,2}-([0-9]){1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}$")


class ChangeTaskNameIn(BaseModel):
    new_name: str
