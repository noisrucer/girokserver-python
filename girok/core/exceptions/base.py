class BaseCustomException(Exception):
    error_code: int
    status_code: int
    detail: str

    def __init__(self, error_code: int, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.error_code = error_code
        self.status_code = status_code
        self.detail = detail

    def __str__(self) -> str:
        return f"[{self.error_code}] status_code: {self.status_code}, detail: {self.detail}"


# """
# To create a concrete exception:

# class InvalidEmailError(BaseCustomException):
#     status_code = 404

#     def __init__(self, detail: str):
#         super().__init__(self.status_code, detail)
# """


# # Root classification
# class BaseAuthException(BaseCustomException):
#     status_code: int = status.HTTP_401_UNAUTHORIZED

#     def __init__(self, detail: str) -> None:
#         super().__init__(self.status_code, detail)


# class BaseTokenException(BaseCustomException):
#     status_code: int = status.HTTP_401_UNAUTHORIZED

#     def __init__(self, detail: str) -> None:
#         super().__init__(self.status_code, detail)


# class BaseValidationException(BaseCustomException):
#     status_code: int = status.HTTP_400_BAD_REQUEST

#     def __init__(self, detail: str) -> None:
#         super().__init__(self.status_code, detail)
