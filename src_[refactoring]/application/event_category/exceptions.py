from fastapi import status
from src.shared.exceptions import BaseCustomException


class EmptyCategoryPathError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Empty Category Path Error: Category path cannot be empty."
        )
