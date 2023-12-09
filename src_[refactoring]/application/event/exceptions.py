from fastapi import status
from src.shared.exceptions import BaseCustomException


class InvalidEventError(BaseCustomException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
