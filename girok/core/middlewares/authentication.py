# from fastapi import Request
# from fastapi.responses import JSONResponse
# from starlette.authentication import AuthCredentials, AuthenticationBackend, BaseUser
# from starlette.requests import HTTPConnection

# from peerloop.core.exceptions.middleware import NoAuthenticationError


# def on_auth_error(request: Request, exc: Exception) -> JSONResponse:
#     return JSONResponse(status_code=401, content={"detail": str(exc)})


# class CustomUser(BaseUser):
#     def __init__(self, user_id: int) -> None:
#         self.user_id = user_id

#     @property
#     def is_authenticated(self) -> bool:
#         return self.user_id is not None

#     @property
#     def display_name(self) -> str:
#         return f"USER_ID: {self.user_id}"

#     @property
#     def identity(self) -> str:
#         return f"CustomUser(user_id: {self.user_id})"


# class AuthBackend(AuthenticationBackend):
#     async def authenticate(
#         self,
#         conn: HTTPConnection,
#     ) -> tuple[AuthCredentials, BaseUser] | None:
#         authorization: str | None = conn.headers.get("Authorization")
#         if authorization is None:  # No JWT token is provided
#             raise NoAuthenticationError()
