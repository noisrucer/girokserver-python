from girok.core.exceptions.base import BaseAuthException


class NoAuthenticationError(BaseAuthException):
    detail: str = "No Authentication"

    def __init__(self) -> None:
        super().__init__(self.detail)
