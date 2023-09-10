from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

import src.category.service as category_service
import src.dependencies as glob_dependencies
import src.task.enums as task_enums
import src.task.exceptions as exceptions
import src.task.schemas as schemas
import src.task.service as service
import src.user.models as user_models
from src.database import get_db

router = APIRouter(prefix="/tasks", tags=["task"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskCreateOut)
async def create_task(
    task: schemas.TaskCreateIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    task = task.dict()
    user_id = current_user.user_id
    task.update({"user_id": user_id})
    new_task = service.create_task(db, task)
    return new_task


@router.get(
    "/",
    status_code=status.HTTP_200_OK
    # response_model=schemas.TaskOut
)
async def get_tasks(
    category: list[str]
    | None = Query(
        default=None,
        title="Category",
        description="Full category path of a category. Ex. ['HKU', 'COMP3230'].",
    ),
    start_date: str
    | None = Query(
        default="2000-01-01 00:00:00",
        title="Start date",
        description="Start date. Ex. '2023-01-23 12:00:00'",
        regex="^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}$",
    ),
    end_date: str
    | None = Query(
        default=(datetime.now() + timedelta(days=365 * 10)).strftime("%Y-%m-%d 00:00:00"),
        title="End date",
        description="End date. Ex. '2023-03-23 12:00:00'",
        regex="^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}$",
    ),
    priority: int | None = Query(default=None, title="Priority", ge=1, le=5),
    no_priority: bool = False,
    tag: str | None = Query(default=None, title="Tag"),
    view: task_enums.TaskView | None = Query(default=None, title="View method for tasks"),
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    user_id = current_user.user_id

    # Check start_date <= end_date
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    if start_date > end_date:
        raise exceptions.InvalidDateWindowException(start_date, end_date)

    if category is None:  # ALL tasks regardless of category
        cat_ids = category_service.get_subcategory_ids_by_parent_id(db, user_id, None)  # top most categories
        cat_ids += [None]
    elif category == [""]:  # Only "None category" category
        cat_ids = [None]
    else:  # Specified category
        cat_id, _ = category_service.get_last_cat_id(db, user_id, category)
        cat_ids = [cat_id]

    if view == task_enums.TaskView.category:
        tasks = service.get_tasks_by_category(
            db=db,
            user_id=user_id,
            cat_ids=cat_ids,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            no_priority=no_priority,
            tag=tag,
        )
    elif view == task_enums.TaskView.list:
        tasks = service.get_tasks_as_list(
            db=db,
            user_id=user_id,
            cat_ids=cat_ids,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            no_priority=no_priority,
            tag=tag,
        )
    else:
        raise Exception("Invalid task view!")

    return {"tasks": tasks}


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    user_id = current_user.user_id
    service.delete_task(db, user_id, task_id)


@router.patch(
    "/{task_id}/tag",
    status_code=status.HTTP_200_OK,
)
async def change_task_tag(
    task_id: int,
    tag: schemas.ChangeTaskTagIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    user_id = current_user.user_id
    tag = tag.dict()
    new_tag_name = tag["new_tag_name"]
    updated_task = service.change_task_tag(db, user_id, task_id, new_tag_name)
    return updated_task


@router.patch(
    "/{task_id}/priority",
    status_code=status.HTTP_200_OK,
)
async def change_task_priority(
    task_id: int,
    priority: schemas.ChangeTaskPriorityIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    user_id = current_user.user_id
    priority = priority.dict()
    new_priority = priority["new_priority"]
    updated_task = service.change_task_priority(db, user_id, task_id, new_priority)
    return updated_task


@router.patch("/{task_id}/date", status_code=status.HTTP_200_OK)
async def change_task_date(
    task_id: int,
    data: schemas.ChangeTaskDateIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    user_id = current_user.user_id
    data = data.dict()
    new_date = data["new_date"]
    updated_task = service.change_task_date(db, user_id, task_id, new_date)
    return updated_task


@router.patch("/{task_id}/name", status_code=status.HTTP_200_OK)
async def change_task_name(
    task_id: int,
    data: schemas.ChangeTaskNameIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    user_id = current_user.user_id
    data = data.dict()
    new_name = data["new_name"]
    updated_task = service.change_task_name(db, user_id, task_id, new_name)
    return updated_task


@router.get("/tags", status_code=status.HTTP_200_OK, response_model=schemas.TagOut)
async def get_tags(
    db: Session = Depends(get_db), current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    user_id = current_user.user_id
    tags = service.get_tags(db, user_id)
    return {"tags": tags}


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=schemas.GetSingleTaskOut)
async def get_single_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    user_id = current_user.user_id
    task = service.get_single_task(db, user_id, task_id)
    return task
