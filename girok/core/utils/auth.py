import random
import string

import bcrypt


def hash_password(raw_password: str) -> str:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()


def check_password(raw_password: str, hashed_password: str) -> bool:
    """Checks if a password matches its hash."""
    return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())


def generate_email_verification_code(token_len: int = 6) -> str:
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(token_len))
