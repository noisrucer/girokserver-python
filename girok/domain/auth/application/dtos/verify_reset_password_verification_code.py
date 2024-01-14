from pydantic import BaseModel, Field

from girok.core.base_class.pydantic_model import EmailMixin


class VerifyResetPasswordVerificationCode(BaseModel, EmailMixin):
    verification_code: str = Field(default=..., examples=["JSDKJ3"])
