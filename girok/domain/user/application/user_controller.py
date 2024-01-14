from fastapi import APIRouter, status

from girok.domain.user.application.dtos.create_user import CreateUserRequest

router = APIRouter(tags=["user"])


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
):
    pass
