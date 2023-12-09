from girok.core.exceptions.base import BaseTokenException


class InvalidTokenError(BaseTokenException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
