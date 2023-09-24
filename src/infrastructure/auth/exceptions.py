from fastapi import status

from src.shared.exceptions import BaseCustomException


class InvalidTokenScopeError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Incorrect token scope"


class ExpiredTokenError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Expired signature token"


class InvalidTokenError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Invalid token"


class JWTError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "JWT error"
