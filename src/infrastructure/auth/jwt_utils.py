from datetime import datetime, timedelta

from jose import ExpiredSignatureError, jwt

from src.config import JWTConfig, load_config
from src.infrastructure.auth.exceptions import ExpiredSignatureToken, InvalidTokenType


def load_jwt_config() -> JWTConfig:
    return load_config().jwt


jwt_config = load_jwt_config()


def create_jwt_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access_token"})
    encoded_jwt = jwt.encode(to_encode, jwt_config.SECRET_KEY, algorithm=jwt_config.ALGORITHM)
    return encoded_jwt


def decode_jwt_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM])
        if payload["type"] != "access_token":
            raise InvalidTokenType()
        user_id = payload.get("sub")
        return user_id
    except ExpiredSignatureError:
        raise ExpiredSignatureToken()
