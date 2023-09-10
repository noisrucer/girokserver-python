from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, Field, validator

import src.auth.exceptions as exceptions
import src.user.schemas as user_schemas


class UserCreate(user_schemas.UserBase):
    password: str = Field(default=...)

    @validator("password")
    def password_must_be_valid(cls, v):
        if len(v) > 30 or len(v) < 6:
            raise exceptions.InvalidPasswordLengthException()
        return v


class UserCreateOut(user_schemas.UserBase):
    user_id: int

    class Config:
        orm_mode = True


class VerificationCode(BaseModel):
    email: str
    verification_code: str = Field(default=...)

    @validator("verification_code")
    def verification_code_must_be_valid(cls, v):
        if len(v) != 6:
            raise exceptions.InvalidVerificationCode()
        return v


class VerifyEmail(BaseModel):
    email: str

    @validator("email")
    def email_must_be_valid(cls, v):
        try:
            validation = validate_email(v)
            email = validation.email
        except EmailNotValidError:
            raise exceptions.EmailNotValidException()
        return email


class Token(BaseModel):
    access_token: str
    token_type: str


class UpdateToken(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str | None = None


class ResetPasswordIn(BaseModel):
    new_password: str