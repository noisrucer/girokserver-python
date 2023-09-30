from fastapi import status

from src.shared.exceptions import BaseCustomException


class EventCategoryNotFoundError(BaseCustomException):
    def __init__(self, category_name: str, pid: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category Not Found: {category_name} is not found under parent category id {pid}",
        )


class EventCategoryAlreadyExistsError(BaseCustomException):
    def __init__(self, category_name: str, pid: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category Already Exists: {category_name} already exists under parent category id {pid}",
        )
