from fastapi import status

from girok.core.exceptions.base import BaseCustomException


class UserAlreadyRegisteredError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, email: str) -> None:
        super().__init__(self.status_code, f"User already registered: {email}")


class EmailNotVerifiedError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, email: str) -> None:
        super().__init__(self.status_code, f"Email not verified: {email}")
