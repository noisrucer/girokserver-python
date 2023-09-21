from fastapi import APIRouter, Depends, status

from src.application.auth.dtos import (
    RegisterRequest,
    RegisterResponse,
    VerifyEmailRequest,
)
from src.dependencies.user_dependencies import get_user_service
from src.domain.user.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
async def register(request: RegisterRequest, user_service: UserService = Depends(get_user_service)):
    new_user_entity = await user_service.register_user(email=request.email, password=request.password)
    return RegisterResponse(user_id=new_user_entity.user_id, email=new_user_entity.email)


@router.post("/verifications", status_code=status.HTTP_204_NO_CONTENT)
def verify_email(request: VerifyEmailRequest, user_service: UserService = Depends(get_user_service)):
    user_service.verify_email(email=request.email, verification_code=request.verification_code)
