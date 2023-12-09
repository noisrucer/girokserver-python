from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from girok.domain.user.exceptions import UserNotVerifiedError
from girok.domain.user.models import User
from girok.domain.user.service import UserService

oauth_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/login", scheme_name="JWT")


@inject
async def get_current_user(
    token: Annotated[str, Depends(oauth_bearer)],
    user_service: UserService = Depends(Provide["user_container.user_service"]),
) -> User:
    user_id = user_service.token_manager.decode_token(token=token)
    user = await user_service.get_user_by_id(user_id=int(user_id))
    return user


@inject
async def get_current_verified_user(verified_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not verified_user.is_verified:
        raise UserNotVerifiedError("User Not Verified Error: email verification is required.")
    return verified_user


@inject
async def get_current_verified_user_id(verified_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not verified_user.is_verified:
        raise UserNotVerifiedError("User Not Verified Error: email verification is required.")
    return verified_user.id
