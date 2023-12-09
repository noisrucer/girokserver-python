from girok.core.exceptions.base import BaseValidationException


class InvalidEmailError(BaseValidationException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
