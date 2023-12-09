from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from girok.core.dependencies.auth import get_current_verified_user_id
from girok.domain.category.dtos import DeleteEventCategoryRequest  # noqa F401
from girok.domain.category.dtos import GetAllCategoriesResponse  # noqa F401
from girok.domain.category.dtos import MoveEventCategoryRequest  # noqa F401
from girok.domain.category.dtos import RenameEventCategoryRequest  # noqa F401
from girok.domain.category.dtos import CreateCategoryRequest, CreateCategoryResponse
from girok.domain.category.exceptions import CategoryEmptyPathError
from girok.domain.category.service import CategoryService

router = APIRouter(prefix="/categories", tags=["category"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateCategoryResponse)
@inject
async def create_event_category(
    request: CreateCategoryRequest,
    category_service: CategoryService = Depends(Provide["category_container.category_service"]),
    current_user_id: int = Depends(get_current_verified_user_id),
) -> CreateCategoryResponse:
    print(type(current_user_id))
    color = request.color_hex
    category_path: list = request.path
    if len(category_path) == 0:
        raise CategoryEmptyPathError()
    new_category = await category_service.create_category(
        color=color, category_path=category_path, user_id=current_user_id
    )
    return CreateCategoryResponse(
        name=new_category.name,
        color_hex=new_category.color,
        parent_id=new_category.parent_id,
    )


# @router.get("/", status_code=status.HTTP_200_OK, response_model=GetAllCategoriesResponse)
@router.get("/", status_code=status.HTTP_200_OK)
@inject
async def get_all_categories(
    category_service: CategoryService = Depends(Provide["category_container.category_service"]),
    current_user_id: int = Depends(get_current_verified_user_id),
):
    result = await category_service.get_all_categories(user_id=current_user_id)  # noqa F401
    return {"status": "hello world"}
    # return GetAllCategoriesResponse(result)


# @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_event_category(
#     request: DeleteEventCategoryRequest,
#     event_category_service: EventCategoryService = Depends(get_event_category_service),
#     current_user_id: str = Depends(get_current_verified_user_id),
# ) -> None:
#     path = request.path
#     event_category_service.delete_event_category(path=path, user_id=current_user_id)


# @router.patch("/parent", status_code=status.HTTP_204_NO_CONTENT)
# async def move_event_category(
#     request: MoveEventCategoryRequest,
#     event_category_service: EventCategoryService = Depends(get_event_category_service),
#     current_user_id: str = Depends(get_current_verified_user_id),
# ) -> None:
#     path = request.path
#     new_parent_path = request.new_parent_path
#     event_category_service.move_event_category(path=path, new_parent_path=new_parent_path, user_id=current_user_id)


# @router.patch("/name", status_code=status.HTTP_204_NO_CONTENT)
# async def rename_event_category(
#     request: RenameEventCategoryRequest,
#     event_category_service: EventCategoryService = Depends(get_event_category_service),
#     current_user_id: str = Depends(get_current_verified_user_id),
# ) -> None:
#     path = request.path
#     new_name = request.new_name
#     event_category_service.rename_event_category(path=path, new_name=new_name, user_id=current_user_id)
