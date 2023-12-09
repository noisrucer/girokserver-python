from datetime import datetime, timedelta

import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)

from girok.core.exceptions.token import InvalidTokenError as CustomInvalidTokenError


class TokenManager:
    def __init__(
        self, secret_key: str, algorithm: str, access_token_expire_minutes: int, refresh_token_expire_minutes: int
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes

    def create_access_token(self, sub: str | int) -> str:
        payload = {
            "sub": str(sub),
            "scope": "access_token",
            "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self.secret_key, self.algorithm)

    def create_refresh_token(self, sub: str | int) -> str:
        payload = {
            "sub": str(sub),
            "scope": "refresh_token",
            "exp": datetime.utcnow() + timedelta(minutes=self.refresh_token_expire_minutes),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self.secret_key, self.algorithm)

    def create_tokens(self, sub: str | int) -> tuple[str, str]:
        return self.create_access_token(sub), self.create_refresh_token(sub)

    def decode_token(self, token: str) -> str:
        """Decode a JWT token and return user_id"""
        return self._decode_sub_from_jwt(token, "access_token")

    def refresh_token(self, refresh_token: str) -> str:
        user_id = self._decode_sub_from_jwt(refresh_token, "refresh_token")
        return self.create_access_token(user_id)

    def _decode_sub_from_jwt(self, token: str, expected_scope: str) -> str:
        """sub refers to the user_id"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload["scope"] != expected_scope:
                raise CustomInvalidTokenError("Invalid Token Scope")
            sub = payload["sub"]
            assert isinstance(sub, str)
            return sub
        except ExpiredSignatureError:
            raise CustomInvalidTokenError("Token has been expired.")
        except InvalidSignatureError:
            raise CustomInvalidTokenError("Invalid Token Signature.")
        except InvalidTokenError:
            raise CustomInvalidTokenError("Invalid Token.")
