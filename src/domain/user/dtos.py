from dataclasses import dataclass


@dataclass
class LoginUserServiceResponse:
    access_token: str
    refresh_token: str
