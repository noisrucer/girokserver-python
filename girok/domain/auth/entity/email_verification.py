from datetime import datetime, timedelta


class EmailVerification:
    def __init__(
        self,
        email: str,
        verification_code: str,
        is_verified: bool,
        expiration_time: datetime = datetime.utcnow() + timedelta(minutes=30),
        id: int | None = None,
    ):
        self.id = id
        self.email = email
        self.verification_code = verification_code
        self.is_verified = is_verified
        self.expiration_time = expiration_time

    def check_verified(self) -> bool:
        return self.is_verified

    def verify(self) -> None:
        self.is_verified = True

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expiration_time
