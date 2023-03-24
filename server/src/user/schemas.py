from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Union

import server.src.user.enums as enums
import server.src.utils as glob_utils
import server.src.auth.exceptions as auth_exceptions

class UserBase(BaseModel):
    email: str

    @validator('email')
    def email_must_be_valid(cls, v):
        try:
            validation = validate_email(v)
            email = validation.email
        except EmailNotValidError as e:
            raise auth_exceptions.EmailNotValidException()
        return email

class User(UserBase):
    class Config:
        orm_mode = True
        

    