from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, Field, validator
from src.application.exceptions.auth_exceptions import InvalidEmailError


class GetEmailStatusRequest(BaseModel):
    email: str = Field(default=...)

    @validator("email")
    def email_must_not_valid(cls, v):
        try:
            validation = validate_email(v)
            email = validation.email
        except EmailNotValidError:
            raise InvalidEmailError(email=v)
        return email


class GetEmailStatusResponse(BaseModel):
    is_verified: bool = Field(default=...)
