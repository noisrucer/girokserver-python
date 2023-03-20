import random
import string
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Union
from datetime import datetime, timedelta

import server.src.auth.exceptions as exceptions
import server.src.auth.schemas as schemas
from server.src.auth.config import get_jwt_settings

jwt_settings = get_jwt_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(raw_password):
    return pwd_context.hash(raw_password)


def verify_password(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)


def generate_verification_code(len=6):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(len))


def hash_verification_code(raw_verification_code):
    return pwd_context.hash(raw_verification_code)


def verify_code(raw_verification_code, hashed_verification_code):
    return pwd_context.verify(raw_verification_code, hashed_verification_code)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire
    })
    encoded_jwt = jwt.encode(to_encode, jwt_settings.ACCESS_SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_settings.REFRESH_TOKEN_EXPIRE_MINUTES)        
    to_encode.update({
        "exp": expire
    })
    encoded_jwt = jwt.encode(to_encode, jwt_settings.REFRESH_SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str):
    try:
        user_email = decode_refresh_jwt(token)
        
        if user_email is None:
            raise exceptions.CredentialsException()
        token_data = schemas.TokenData(username=user_email)
    except JWTError:
        raise exceptions.CredentialsException()
    
    return token_data


def get_new_access_token(token: str):
    token_data = verify_refresh_token(token)
    return create_access_token(token_data)


def decode_access_jwt(token):
    payload = jwt.decode(token, jwt_settings.ACCESS_SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
    email: str = payload.get("sub")
    return email


def decode_refresh_jwt(token):
    payload = jwt.decode(token, jwt_settings.REFRESH_SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
    email: str = payload.get("sub")
    return email

    
def read_html_content_and_replace(
    replacements: dict[str, str],
    html_path: str = "server/src/email/verification.html"
):
    f = open(html_path)
    content = f.read()
    for target, val in replacements.items():
        content = content.replace(target, val)
    f.close()
    return content