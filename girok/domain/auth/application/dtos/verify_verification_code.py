from pydantic import BaseModel, Field

from girok.core.base_class.pydantic_model import EmailMixin


class VerifyEmailVerificationCodeRequest(BaseModel, EmailMixin):
    email: str = Field(default=..., examples=["changjin9792@gmail.com"])
    verification_code: str = Field(default=..., examples=["JSDKJ3"])
