import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.config import load_config
from src.infrastructure.auth.auth_handler import AuthHandler
from src.infrastructure.auth.exceptions import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", scheme_name="JWT")

cfg = load_config()
auth_handler = AuthHandler(jwt_config=cfg.jwt)


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        user_id = auth_handler.decode_token(token)
        return user_id
    except jwt.PyJWTError:
        raise JWTError()


def get_token(token: str = Depends(oauth2_scheme)):
    return token
