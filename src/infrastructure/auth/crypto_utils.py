from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_data(raw: str) -> str:
    return pwd_context.hash(raw)


def verify_data(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)
