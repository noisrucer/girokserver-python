from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, validator

import src.auth.exceptions as auth_exceptions


class UserBase(BaseModel):
    email: str

    @validator("email")
    def email_must_be_valid(cls, v):
        try:
            validation = validate_email(v)
            email = validation.email
        except EmailNotValidError:
            raise auth_exceptions.EmailNotValidException()
        return email


class User(UserBase):
    class Config:
        orm_mode = True
