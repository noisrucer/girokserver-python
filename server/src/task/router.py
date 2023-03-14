from typing import List, Union
import pprint

from datetime import datetime, timedelta

from fastapi import APIRouter, status, Depends, Query
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
    min_pri: Union[int, None] = Query(
        default=None,
        title="Minimum priority",
        ge=1,
        le=5
    ),
    max_pri: Union[int, None] = Query(
        default=None,
        title="Maximum priority",
        ge=1,
        le=5
    ),
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
    
    # min_pri and max_pri must be both None or int 
    if bool(min_pri) ^ bool(max_pri):
        raise exceptions.InvalidPriorityPairException()
    
    # Check min_pri <= max_pri
    if all([min_pri, max_pri]) and min_pri > max_pri:
        raise exceptions.InvalidPriorityWindowException()
        
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
            min_pri=min_pri,
            max_pri=max_pri,
            tag=tag
        )
    elif view == task_enums.TaskView.list:
        tasks = service.get_tasks_as_list(
            db=db,
            user_id=user_id,
            cat_ids=cat_ids,
            start_date=start_date,
            end_date=end_date,
            min_pri=min_pri,
            max_pri=max_pri,
            tag=tag
        )
    else:
        raise Exception("Invalid task view!")
    
    # resp = []
    # for task in tasks:
    #     task_data = {}
    #     for col in task.__table__.columns:
    #         if col.name == "task_category_id" and task.task_category_id is not None:
    #             cat_full_path = category_service.get_category_full_path_by_id(db, user_id, task.task_category_id)
    #             task_data["category_path"] = cat_full_path
    #         if col.name == "deadline":
    #             task_data["deadline"] = task.deadline.strftime("%Y-%m-%d %H:%M:%S")
    #             continue
    #         task_data[col.name] = getattr(task, col.name)
    #     resp.append(task_data)
    pprint.pprint(tasks)
        
    return {"tasks": tasks}
    
    
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
    
    
    

    
    