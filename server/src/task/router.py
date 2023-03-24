from typing import List, Union
import pprint

from datetime import datetime, timedelta

from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.orm import Session

from server.src.database import get_db
import server.src.task.schemas as schemas
import server.src.utils as general_utils
import server.src.task.service as service
import server.src.user.service as user_service
import server.src.category.service as category_service
import server.src.user.models as user_models
import server.src.task.exceptions as exceptions
import server.src.dependencies as glob_dependencies
import server.src.task.enums as task_enums


router = APIRouter(
    prefix="/tasks",
    tags=["task"]
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.TaskCreateOut
)
async def create_task(
    task: schemas.TaskCreateIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    task = task.dict()
    user_id = current_user.user_id
    task.update({'user_id': user_id})
    new_task = service.create_task(db, task)
    return new_task
    

@router.get(
    "/",
    status_code=status.HTTP_200_OK
    # response_model=schemas.TaskOut
)
async def get_tasks(
    category: Union[List[str], None] = Query(
        default=None,
        title="Category",
        description="Full category path of a category. Ex. ['HKU', 'COMP3230'].",
    ),
    start_date: Union[str, None] = Query(
        default="2000-01-01 00:00:00",
        title="Start date",
        description="Start date. Ex. '2023-01-23 12:00:00'",
        regex="^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"
    ),
    end_date: Union[str, None] = Query(
        default=(datetime.now() + timedelta(days=365*10)).strftime("%Y-%m-%d 00:00:00"),
        title="End date",
        description="End date. Ex. '2023-03-23 12:00:00'",
        regex="^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"
    ),
    priority: Union[int, None] = Query(
        default=None,
        title="Priority",
        ge=1,
        le=5
    ),
    no_priority: bool = False,
    tag: Union[str, None] = Query(
        default=None,
        title="Tag"
    ),
    view: Union[task_enums.TaskView, None]= Query(
        default=None,
        title="View method for tasks"  
    ),
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    user_id = current_user.user_id
        
    # Check start_date <= end_date
    start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    if start_date > end_date:
        raise exceptions.InvalidDateWindowException(start_date, end_date)
    
    if category is None: # ALL tasks regardless of category
        cat_ids = category_service.get_subcategory_ids_by_parent_id(db, user_id, None) # top most categories
        cat_ids += [None]
    elif category == ['']: # Only "None category" category
        cat_ids = [None]
    else: # Specified category
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
            tag=tag
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
            tag=tag
        )
    else:
        raise Exception("Invalid task view!")
        
    return {"tasks": tasks}
    
    
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    user_id = current_user.user_id
    service.delete_task(db, user_id, task_id)
    
    
@router.patch(
    '/{task_id}/tag',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_task_tag(
    task_id: int,
    tag: schemas.ChangeTaskTagIn,
    db: Session=Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user) 
):
    user_id = current_user.user_id
    tag = tag.dict()
    new_tag_name = tag['new_tag_name']
    service.change_task_tag(db, user_id, task_id, new_tag_name)


@router.patch(
    '/{task_id}/priority',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_task_priority(
    task_id: int,
    priority: schemas.ChangeTaskPriorityIn,
    db: Session=Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user) 
):
    user_id = current_user.user_id
    priority = priority.dict()
    new_priority = priority['new_priority']
    service.change_task_priority(db, user_id, task_id, new_priority)


@router.patch(
    '/{task_id}/date',
    status_code=status.HTTP_204_NO_CONTENT
)
async def change_task_date(
    task_id: int,
    data: schemas.ChangeTaskDateIn,
    db: Session=Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user) 
):
    user_id = current_user.user_id
    data = data.dict()
    new_date = data['new_date']
    service.change_task_date(db, user_id, task_id, new_date)


@router.get(
    '/tags',
    status_code=status.HTTP_200_OK,
    response_model=schemas.TagOut
)
async def get_tags(
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    user_id = current_user.user_id
    tags = service.get_tags(db, user_id)
    return {"tags": tags}


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.GetSingleTaskOut
)
async def get_single_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    user_id = current_user.user_id
    task = service.get_single_task(db, user_id, task_id)
    return task
