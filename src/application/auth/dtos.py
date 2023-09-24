from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, Field, validator

from src.application.exceptions.auth_exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
)


class RegisterRequest(BaseModel):
    email: str = Field(default=...)
    password: str = Field(default=..., min_length=6, max_length=30)  # TODO: Add regex for password validation

    @validator("email")
    def email_must_not_valid(cls, v):
        try:
            validation = validate_email(v)
            email = validation.email
        except EmailNotValidError:
            raise InvalidEmailError(email=v)
        return email

    @validator("password")
    def password_must_be_valid(cls, v):
        if len(v) > 30 or len(v) < 6:
            raise InvalidPasswordError(password=v)
        return v


class RegisterResponse(BaseModel):
    user_id: int = Field(default=...)
    email: str = Field(default=...)


class VerifyEmailRequest(BaseModel):
    email: str = Field(default=...)
    verification_code: str = Field(default=...)

    @validator("email")
    def email_must_be_valid(cls, v):
        try:
            validation = validate_email(v)
            email = validation.email
        except EmailNotValidError:
            raise InvalidEmailError(email=v)
        return email


class LoginRequest(BaseModel):  # TODO: Remove redundancy -> Use EmailBaseModel
    email: str = Field(default=...)
    password: str = Field(default=...)

    @validator("email")
    def email_must_be_valid(cls, v):
        try:
            validation = validate_email(v)
            email = validation.email
        except EmailNotValidError:
            raise InvalidEmailError(email=v)
        return email


class LoginResponse(BaseModel):
    access_token: str = Field(default=...)
    token_type: str = Field(default="bearer")
    # refresh_token: str = Field(default=...)
