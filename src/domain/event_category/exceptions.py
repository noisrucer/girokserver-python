from fastapi import status

from src.shared.exceptions import BaseCustomException


class EventCategoryNotFoundError(BaseCustomException):
    def __init__(self, super_category_path: str, category_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category Not Found: '{super_category_path}' does not have a sub-category named '{category_name}'",  # noqa: E501
        )


class EventCategoryAlreadyExistsError(BaseCustomException):
    def __init__(self, super_category_path: str, category_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category Already Exists: '{super_category_path}' already has a sub-category named '{category_name}'",  # noqa: E501
        )


class EmptyCategoryPathError(BaseCustomException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category Path is Empty: Category path must contain at least one category name"
            if detail is None
            else detail,  # noqa: E501
        )
