from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from girok.domain.auth.dtos import RefreshTokenRequest, RefreshTokenResponse
from girok.domain.auth.service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/refresh-token", status_code=status.HTTP_200_OK, response_model=RefreshTokenResponse)
@inject
async def refresh_token(
    request: RefreshTokenRequest, auth_service: AuthService = Depends(Provide["auth_container.auth_service"])
) -> RefreshTokenResponse:
    new_access_token = auth_service.refresh_token(request.refresh_token)
    return RefreshTokenResponse(access_token=new_access_token)
