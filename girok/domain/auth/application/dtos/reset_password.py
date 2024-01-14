from pydantic import BaseModel, Field, validator

from girok.core.base_class.pydantic_model import EmailMixin
from girok.core.exceptions.emitter import raise_custom_exception
from girok.domain.exceptions import DomainExceptions


class ResetPasswordRequest(BaseModel, EmailMixin):
    email: str = Field(default=..., examples=["changjin9792@gmail.com"])
    new_password: str = Field(default=..., examples=["Asdfk123*"], min_length=6, max_length=50)
    verification_code: str = Field(default=..., examples=["JSDKJ3"])

    @validator("new_password")
    def password_must_be_valid(cls, v: str) -> str:
        """
        Rules
        1) Must be 6 <= len(pwd) <= 50
        2) Must contain at least one capital letter
        3) Must contain at least one lower-case letter
        4) Must contain at least one special character. One of (@, #, $, %, *, !)
        """
        if len(v) < 6 or len(v) > 50:
            raise_custom_exception(DomainExceptions.INVALID_PASSWORD)
            # raise InvalidPasswordFormatError("Password must be 6 <= len(pwd) <= 50")
        if not any(char.isupper() for char in v):
            raise_custom_exception(DomainExceptions.INVALID_PASSWORD)
            # raise InvalidPasswordFormatError("Password must contain at least one capital letter")
        if not any(char.islower() for char in v):
            raise_custom_exception(DomainExceptions.INVALID_PASSWORD)
            # raise InvalidPasswordFormatError("Password must contain at least one lower-case letter")
        if not any(char in ["@", "#", "$", "%", "*", "!"] for char in v):
            raise_custom_exception(DomainExceptions.INVALID_PASSWORD)
            # raise InvalidPasswordFormatError(
            #     "Password must contain at least one special character. One of (@, #, $, %, *, !)"
            # )
        return v
