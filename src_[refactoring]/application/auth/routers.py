from fastapi import APIRouter, Depends, status
from src.application.auth.dtos import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    SendEmailVerificationCodeRequest,
    SignupRequest,
    VerifyEmailRequest,
    VerifyEmailVerificationCodeRequest,
)
from src.dependencies.auth_dependencies import get_current_user_id
from src.dependencies.user_dependencies import get_user_service
from src.domain.user.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/emailVerification", status_code=status.HTTP_204_NO_CONTENT)
async def send_email_verification_code(
    request: SendEmailVerificationCodeRequest, user_service: UserService = Depends(get_user_service)
):
    await user_service.send_email_verification_code(email=request.email)


@router.post("/emailVerificationCheck", status_code=status.HTTP_204_NO_CONTENT)
def verify_email_verification_code(
    request: VerifyEmailVerificationCodeRequest, user_service: UserService = Depends(get_user_service)
):
    user_service.verify_email_verification_code(email=request.email, verification_code=request.verification_code)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(request: SignupRequest, user_service: UserService = Depends(get_user_service)):
    user_service.signup(email=request.email, password=request.password, verification_code=request.verification_code)


# @router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
# async def register(request: RegisterRequest, user_service: UserService = Depends(get_user_service)):
#     new_user_entity = await user_service.register_user(email=request.email, password=request.password)
#     return RegisterResponse(user_id=new_user_entity.user_id, email=new_user_entity.email)


@router.post("/verifications", status_code=status.HTTP_204_NO_CONTENT)
def verify_email(request: VerifyEmailRequest, user_service: UserService = Depends(get_user_service)):
    user_service.verify_email(email=request.email, verification_code=request.verification_code)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(request: LoginRequest, user_service: UserService = Depends(get_user_service)):
    login_service_response = user_service.login_user(email=request.email, password=request.password)
    access_token = login_service_response.access_token
    refresh_token = login_service_response.refresh_token
    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh_token", status_code=status.HTTP_200_OK, response_model=RefreshTokenResponse)
def refresh_token(request: RefreshTokenRequest, user_service: UserService = Depends(get_user_service)):
    access_token = user_service.refresh_token(refresh_token=request.refresh_token)
    return RefreshTokenResponse(access_token=access_token)


@router.post("/protected")
def protect(current_user_id: str = Depends(get_current_user_id)):
    return {"current_user_id": current_user_id}
