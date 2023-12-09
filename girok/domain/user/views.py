from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from girok.core.dependencies.auth import get_current_user, get_current_verified_user
from girok.core.exceptions.validation import InvalidEmailError
from girok.core.utils.validation import is_valid_email_format
from girok.domain.user.dtos import (
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
    VerifyEmailRequest,
)
from girok.domain.user.models import User
from girok.domain.user.service import UserService

router = APIRouter(tags=["user"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
@inject
async def register(
    request: RegisterRequest, user_service: UserService = Depends(Provide["user_container.user_service"])
) -> RegisterResponse:
    await user_service.create_user(email=request.email, password=request.password)
    return RegisterResponse(email=request.email)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
@inject
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(Provide["user_container.user_service"]),
) -> LoginResponse:
    if not is_valid_email_format(request.username):
        raise InvalidEmailError(f"Invalid Email Error: {request.username} is not a valid email address.")
    resp = await user_service.login(email=request.username, password=request.password)
    access_token = resp["access_token"]
    refresh_token = resp["refresh_token"]
    return LoginResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post(
    "/verifications",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def verify_email(
    request: VerifyEmailRequest, user_service: UserService = Depends(Provide["user_container.user_service"])
) -> None:
    await user_service.verify_email(email=request.email, verification_code=request.verification_code)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
@inject
async def get_me(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user


@router.get("/verified-me", status_code=status.HTTP_200_OK, response_model=UserResponse)
@inject
async def get_verified_me(user: Annotated[User, Depends(get_current_verified_user)]) -> User:
    return user
