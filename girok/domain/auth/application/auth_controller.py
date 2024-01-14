from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from girok.domain.auth.application.dtos.check_email_registered import (
    CheckEmailRegisteredRequest,
)
from girok.domain.auth.application.dtos.login import LoginRequest, LoginResponse
from girok.domain.auth.application.dtos.refresh_token import (
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from girok.domain.auth.application.dtos.send_verification_code import (
    SendEmailVerificationCodeRequest,
)
from girok.domain.auth.application.dtos.signup import SignupRequest
from girok.domain.auth.application.dtos.verify_verification_code import (
    VerifyEmailVerificationCodeRequest,
)
from girok.domain.auth.facade.auth_facade import AuthFacade

router = APIRouter(tags=["auth"])


@router.post("/auth/verification-code", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def send_verification_code(
    request: SendEmailVerificationCodeRequest, auth_facade: AuthFacade = Depends(Provide["auth_container.auth_facade"])
):
    await auth_facade.send_email_verification_code(email=request.email)


@router.post("/auth/verification-code/check", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def verify_verification_code(
    request: VerifyEmailVerificationCodeRequest,
    auth_facade: AuthFacade = Depends(Provide["auth_container.auth_facade"]),
):
    await auth_facade.verify_email_verification_code(email=request.email, code=request.verification_code)


@router.post("/users", status_code=status.HTTP_201_CREATED)
@inject
async def register(
    request: SignupRequest,
    auth_facade: AuthFacade = Depends(Provide["auth_container.auth_facade"]),
):
    await auth_facade.register(
        email=request.email, password=request.password, verification_code=request.verification_code
    )


@router.get("/auth/email/registered", status_code=status.HTTP_200_OK)
@inject
async def check_email_registered(
    email: str,
    auth_facade: AuthFacade = Depends(Provide["auth_container.auth_facade"]),
):
    is_email_registered = await auth_facade.check_email_registered(email=email)
    return CheckEmailRegisteredRequest(is_registered=is_email_registered)


@router.post("/auth/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
@inject
async def login(
    request: LoginRequest,
    auth_facade: AuthFacade = Depends(Provide["auth_container.auth_facade"]),
):
    access_token, refresh_token = await auth_facade.login(email=request.email, password=request.password)
    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/auth/refresh-token", status_code=status.HTTP_200_OK, response_model=RefreshTokenResponse)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    auth_facade: AuthFacade = Depends(Provide["auth_container.auth_facade"]),
):
    access_token = await auth_facade.refresh_token(refresh_token=request.refresh_token)
    return RefreshTokenResponse(access_token=access_token)
