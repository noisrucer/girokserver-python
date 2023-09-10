from email_validator import EmailNotValidError, validate_email
from pydantic import EmailStr
from sqlalchemy.orm import Session

import src.auth.exceptions as exceptions
import src.auth.utils as utils
import src.user.models as user_models


def get_user_by_email(db: Session, email: EmailStr):
    user = db.query(user_models.User).filter(user_models.User.email == email).first()
    return user


def get_password_by_email(db: Session, email: EmailStr):
    user = db.query(user_models.User).filter(user_models.User.email == email).first()
    return user.password


def get_current_active_user(db: Session, email: EmailStr, is_activate: bool):
    return (
        db.query(user_models.User)
        .filter(user_models.User.email == email, user_models.User.is_activate == is_activate)
        .first()
    )


def get_refresh_token(db: Session, email: EmailStr):
    user = db.query(user_models.User).filter(user_models.User.email == email).first()
    return user.refresh_token


def authenticate_user(db: Session, email: str, password: str):
    try:
        validation = validate_email(email)
        email = validation.email
    except EmailNotValidError:
        raise exceptions.EmailNotValidException()

    user = db.query(user_models.User).filter(user_models.User.email == email).first()
    if not user:
        return False
    if not user.is_activate:
        raise exceptions.EmailNotValidatedException()
    if not utils.verify_password(password, user.password):
        raise exceptions.InvalidEmailOrPasswordException()
    return user
