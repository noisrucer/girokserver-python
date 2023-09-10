import random
import string
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import src.auth.exceptions as exceptions
import src.auth.schemas as schemas
from src.auth.config import get_jwt_settings

jwt_settings = get_jwt_settings()

security = HTTPBearer()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(raw_password):
    return pwd_context.hash(raw_password)


def verify_password(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)


def generate_verification_code(token_len=6):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(token_len))


def hash_verification_code(raw_verification_code):
    return pwd_context.hash(raw_verification_code)


def verify_code(raw_verification_code, hashed_verification_code):
    return pwd_context.verify(raw_verification_code, hashed_verification_code)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "type": "access_token"
    })
    encoded_jwt = jwt.encode(to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_settings.REFRESH_TOKEN_EXPIRE_MINUTES)        
    to_encode.update({
        "exp": expire,
        "type": "refresh_token"
    })
    encoded_jwt = jwt.encode(to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return encoded_jwt


def decode_access_jwt(token):
    try:
        payload = jwt.decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
        if payload["type"] != "access_token":
            raise exceptions.InvalidTokenType()
        email: str = payload.get("sub")
        return email
    except ExpiredSignatureError:
        raise exceptions.ExpiredSignatureToken()
        
    
def decode_refresh_jwt(token):
    try:
        payload = jwt.decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
        if payload["type"] != "refresh_token":
            raise exceptions.InvalidTokenType()
        email: str = payload.get("sub")
        return email
    except ExpiredSignatureError:
        raise exceptions.ExpiredSignatureToken()
    

def auth_access_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
		return decode_access_jwt(auth.credentials)


def auth_refresh_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
		return decode_refresh_jwt(auth.credentials)

    
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