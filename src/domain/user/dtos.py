from dataclasses import dataclass


@dataclass
class LoginUserServiceResponse:
    access_token: str
    token_type: str
