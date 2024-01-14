from pydantic import BaseModel, Field

from girok.core.base_class.pydantic_model import EmailMixin, PasswordMixin


class SignupRequest(BaseModel, EmailMixin, PasswordMixin):
    email: str = Field(default=..., examples=["changjin9792@gmail.com"])
    password: str = Field(default=..., examples=["Asdfk123*"], min_length=6, max_length=50)
    verification_code: str = Field(default=..., examples=["JSDKJ3"])
