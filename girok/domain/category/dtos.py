from pydantic import BaseModel, Field, RootModel

from girok.core.shared.constants import DEFAULT_CATEGORY_COLOR


class CreateCategoryRequest(BaseModel):
    color_hex: str = Field(
        default=DEFAULT_CATEGORY_COLOR, description="Color of the event category in hexadecimal", examples=["#83887b"]
    )
    path: list[str] = Field(
        default=..., description="New path of the event category", examples=[["HKU", "COMP3230", "Assignment"]]
    )


class CreateCategoryResponse(BaseModel):
    name: str = Field(..., description="Name of the newly created event category")
    color_hex: str = Field(..., description="Color of the newly created event category in hexadecimal")
    parent_id: int | None = Field(
        ..., description="ID of the parent event category of the newly created event category"
    )


class Category(BaseModel):
    subcategories: dict[str, "Category"]
    color: str


class GetAllCategoriesResponse(RootModel):
    root: dict[str, Category]


class DeleteEventCategoryRequest(BaseModel):
    path: list[str] = Field(
        default=...,
        description="Target path of the category to be deleted",
        examples=[["HKU", "COMP3230", "Assignment"]],
    )


class MoveEventCategoryRequest(BaseModel):
    path: list[str] = Field(
        default=..., description="Target path of the category to be moved", examples=[["HKU", "COMP3230", "Assignment"]]
    )
    new_parent_path: list[str] = Field(
        default=...,
        description="New path of the parent category of the category to be moved",
        examples=[["Study", "Coding"]],
    )


class RenameEventCategoryRequest(BaseModel):
    path: list[str] = Field(
        default=...,
        description="Target path of the category to be renamed",
        examples=[["HKU", "COMP3230", "Assignment"]],
    )
    new_name: str = Field(default=..., description="New name of the category to be renamed", examples=["Asg"])
