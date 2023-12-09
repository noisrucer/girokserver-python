from fastapi import status

from girok.core.exceptions.base import BaseCustomException


class InvalidPasswordFormatError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)


class DuplicateEmailError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)


class UserDoesNotExistError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)


class UserAlreadyExistsError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)


class UserNotVerifiedError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str) -> None:
        super().__init__(self.status_code, detail)


class IncorrectPasswordError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect password"

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)


class VerificationCodeExpiredError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Verification code has expired"

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)


class VerificationCodeDoesNotExistError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Verification code does not exist"

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)


class InvalidVerificationCodeError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid verification code"

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)
