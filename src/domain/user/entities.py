from datetime import datetime


class UserEntity:
    def __init__(self, email: str, hashed_password: str, is_verified: bool = False, user_id: int = None):
        self.email = email
        self.hashed_password = hashed_password
        self.is_verified = is_verified
        self.user_id = user_id

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_verified": self.is_verified,
            "user_id": self.user_id,
        }

    def assign_user_id(self, user_id: int) -> None:
        self.user_id = user_id

    def verify(self) -> None:
        self.is_verified = True


class EmailVerificationEntity:
    def __init__(self, user_id: int, verification_code: str, expiration_time: datetime):
        self.user_id = user_id
        self.verification_code = verification_code
        self.expiration_time = expiration_time
