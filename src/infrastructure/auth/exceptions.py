from fastapi import status

from src.shared.exceptions import BaseCustomException


class InvalidTokenType(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Incorrect token type"


class ExpiredSignatureToken(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Expired signature token"
