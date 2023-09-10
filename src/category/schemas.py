from pydantic import BaseModel


class CategoryIn(BaseModel):
    user_email: str


class CategoryOut(BaseModel):
    resp: dict[str, dict]


class CategoryCreateIn(BaseModel):
    color: str | None
    names: list[str]


class CategoryCreateOut(BaseModel):
    task_category_id: int

    class Config:
        orm_mode = True


class CategoryDeleteIn(BaseModel):
    cats: list[str]


class CategoryRenameIn(BaseModel):
    cats: list[str]
    new_name: str


class CategoryMoveIn(BaseModel):
    cats: list[str]
    new_parent_cats: list[str]


class LastCategoryIdIn(BaseModel):
    cats: list[str]
