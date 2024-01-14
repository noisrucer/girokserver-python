from girok.core.utils.auth import hash_password


class User:
    def __init__(
        self,
        email: str,
        password: str,
        id: int | None = None,
    ):
        self.id = id
        self.email = email
        self.password = password

    def hash_password(self):
        self.password = hash_password(self.password)
