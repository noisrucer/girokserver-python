from fastapi import status
from src.shared.exceptions import BaseCustomException


class DuplicatedEmailError(BaseCustomException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Already Existing Email Address: {email} is already registered.",
        )


class UserNotFoundError(BaseCustomException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User Not Found: {email} is not registered.",
        )


class UserAlreadyVerifiedError(BaseCustomException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User Already Verified: {email} is already verified.",
        )


class UserNotVerifiedError(BaseCustomException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User Not Verified: {email} is not verified.",
        )


class InvalidPasswordError(BaseCustomException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password.")


class InvalidVerificationCodeError(BaseCustomException):
    def __init__(self, verification_code: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Verification Code: {verification_code} is not valid.",
        )


class VerificationCodeExpiredError(BaseCustomException):
    def __init__(self, verification_code: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Verification Code Expired: {verification_code} has expired.",
        )
