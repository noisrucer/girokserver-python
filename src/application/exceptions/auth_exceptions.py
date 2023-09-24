from src.shared.exceptions import BaseCustomException


class InvalidEmailError(BaseCustomException):
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f"Invalid Email Error: {email} is not a valid email address.")


class InvalidPasswordError(BaseCustomException):
    def __init__(self, password: str):
        super().__init__(
            status_code=400,
            detail=f"Invalid Password Error: {password} is not a valid password. It must be 6 ~ 30 characters.",
        )
