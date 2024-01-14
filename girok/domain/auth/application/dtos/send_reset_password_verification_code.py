from pydantic import BaseModel

from girok.core.base_class.pydantic_model import EmailMixin


class SendResetPasswordEmailVerificationCodeRequest(BaseModel, EmailMixin):
    pass
