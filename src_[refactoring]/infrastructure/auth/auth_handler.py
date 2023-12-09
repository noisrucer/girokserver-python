from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from src.config import JWTConfig
from src.infrastructure.auth.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    InvalidTokenScopeError,
)


class AuthHandler:
    def __init__(self, jwt_config: JWTConfig):
        self.jwt_config = jwt_config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_data(self, raw: str) -> str:
        return self.pwd_context.hash(raw)

    def verify_data(self, raw: str, hashed: str) -> bool:
        return self.pwd_context.verify(raw, hashed)

    def create_access_token(self, sub: str | int) -> str:
        payload = {
            "sub": str(sub),
            "scope": "access_token",
            "exp": datetime.utcnow() + timedelta(minutes=self.jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self.jwt_config.SECRET_KEY, algorithm=self.jwt_config.ALGORITHM)

    def create_refresh_token(self, sub: str | int) -> str:
        payload = {
            "sub": str(sub),
            "scope": "refresh_token",
            "exp": datetime.utcnow() + timedelta(days=self.jwt_config.REFRESH_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self.jwt_config.SECRET_KEY, algorithm=self.jwt_config.ALGORITHM)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.jwt_config.SECRET_KEY, algorithms=[self.jwt_config.ALGORITHM])
            if payload["scope"] != "access_token":
                raise InvalidTokenScopeError()
            user_id = payload["sub"]
            return user_id
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    def refresh_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, self.jwt_config.SECRET_KEY, algorithms=[self.jwt_config.ALGORITHM])
            if payload["scope"] != "refresh_token":
                raise InvalidTokenScopeError()
            user_id = payload["sub"]
            new_token = self.create_access_token(sub=user_id)
            return new_token
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()
