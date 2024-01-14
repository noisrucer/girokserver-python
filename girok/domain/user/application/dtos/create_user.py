from pydantic import BaseModel, Field

from girok.core.base_class.pydantic_model import EmailMixin, PasswordMixin


class CreateUserRequest(BaseModel, EmailMixin, PasswordMixin):
    email: str = Field(default=..., examples=["changjin9792@gmail.com"])
    password: str = Field(default=..., examples=["Aksdf123*"])
    verification_code: str = Field(default=..., examples=["JSDKJ3"])
