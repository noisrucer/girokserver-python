from pydantic import BaseModel, Field

from girok.core.base_class.pydantic_model import EmailMixin, PasswordMixin


class LoginRequest(BaseModel, EmailMixin, PasswordMixin):  # TODO: Remove redundancy -> Use EmailBaseModel
    pass


class LoginResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
