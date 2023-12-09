from fastapi import APIRouter, Depends, status
from src.application.user.dtos import GetEmailStatusRequest, GetEmailStatusResponse
from src.dependencies.user_dependencies import get_user_service
from src.domain.user.services import UserService

router = APIRouter(tags=["user"])


@router.post("/email/status", status_code=status.HTTP_200_OK, response_model=GetEmailStatusResponse)
def get_email_status(
    request: GetEmailStatusRequest,
    user_service: UserService = Depends(get_user_service),
):
    is_verified = user_service.is_email_verified(email=request.email)
    return GetEmailStatusResponse(is_verified=is_verified)
