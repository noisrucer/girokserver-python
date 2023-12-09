from girok.core.authentication.token_manager import TokenManager


class AuthService:
    def __init__(self, token_manager: TokenManager) -> None:
        self.token_manager = token_manager

    def refresh_token(self, refresh_token: str) -> str:
        return self.token_manager.refresh_token(refresh_token)
