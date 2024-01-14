from fastapi import APIRouter, Depends, status

from src.application.event_category.dtos import (
    CreateEventCategoryRequest,
    CreateEventCategoryResponse,
    DeleteEventCategoryRequest,
    GetAllCategoriesResponse,
    MoveEventCategoryRequest,
    RenameEventCategoryRequest,
)
from src.application.event_category.exceptions import EmptyCategoryPathError
from src.dependencies.auth_dependencies import get_current_user_id
from src.dependencies.event_category_dependencies import get_event_category_service
from src.domain.event_category.services import EventCategoryService

router = APIRouter(prefix="/categories", tags=["category"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateEventCategoryResponse)
def create_event_category(
    request: CreateEventCategoryRequest,
    event_category_service: EventCategoryService = Depends(get_event_category_service),
    current_user_id: str = Depends(get_current_user_id),
) -> CreateEventCategoryResponse:
    color = request.color_hex
    category_path: list = request.path
    if len(category_path) == 0:
        raise EmptyCategoryPathError()
    new_event_category_entity = event_category_service.create_event_category(
        color=color, category_path=category_path, user_id=current_user_id
    )
    return CreateEventCategoryResponse(
        name=new_event_category_entity.name,
        color_hex=new_event_category_entity.color,
        parent_event_category_id=new_event_category_entity.parent_event_category_id,
    )


@router.get("/", status_code=status.HTTP_200_OK, response_model=GetAllCategoriesResponse)
def get_all_event_categories(
    event_category_service: EventCategoryService = Depends(get_event_category_service),
    current_user_id: str = Depends(get_current_user_id),
) -> GetAllCategoriesResponse:
    result = event_category_service.get_all_categories(user_id=current_user_id)
    return GetAllCategoriesResponse(root=result)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_event_category(
    request: DeleteEventCategoryRequest,
    event_category_service: EventCategoryService = Depends(get_event_category_service),
    current_user_id: str = Depends(get_current_user_id),
) -> None:
    path = request.path
    event_category_service.delete_event_category(path=path, user_id=current_user_id)


@router.patch("/parent", status_code=status.HTTP_204_NO_CONTENT)
def move_event_category(
    request: MoveEventCategoryRequest,
    event_category_service: EventCategoryService = Depends(get_event_category_service),
    current_user_id: str = Depends(get_current_user_id),
) -> None:
    path = request.path
    new_parent_path = request.new_parent_path
    event_category_service.move_event_category(path=path, new_parent_path=new_parent_path, user_id=current_user_id)


@router.patch("/name", status_code=status.HTTP_204_NO_CONTENT)
def rename_event_category(
    request: RenameEventCategoryRequest,
    event_category_service: EventCategoryService = Depends(get_event_category_service),
    current_user_id: str = Depends(get_current_user_id),
) -> None:
    path = request.path
    new_name = request.new_name
    event_category_service.rename_event_category(path=path, new_name=new_name, user_id=current_user_id)
