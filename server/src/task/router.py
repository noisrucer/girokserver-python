from typing import List, Union

from datetime import datetime

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from server.src.database import get_db
import server.src.task.schemas as schemas
import server.src.task.service as service
import server.src.user.service as user_service
import server.src.category.service as category_service
import server.src.user.models as user_models
import server.src.task.exceptions as exceptions
import server.src.dependencies as glob_dependencies


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
    status_code=status.HTTP_200_OK,
    response_model=schemas.TaskOut
)
async def get_tasks(
    category: Union[List[str], None] = Query(
        default=None,
        title="Category",
        description="Full category path of a category. Ex. ['HKU', 'COMP3230'].",
    ),
    start_date: Union[str, None] = Query(
        default=None,
        title="Start date",
        description="Start date. Ex. '2023-01-23 12:00:00'",
        regex="^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"
    ),
    end_date: Union[str, None] = Query(
        default=None,
        title="End date",
        description="End date. Ex. '2023-03-23 12:00:00'",
        regex="^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"
    ),
    min_pri: Union[int, None] = Query(
        default=1,
        title="Minimum priority",
        ge=1,
        le=5
    ),
    max_pri: Union[int, None] = Query(
        default=5,
        title="Maximum priority",
        ge=1,
        le=5
    ),
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    # Check min_pri <= max_pri
    if min_pri > max_pri:
        raise exceptions.InvalidPriorityWindowException()
        
    # Check start_date <= end_date
    start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    if start_date > end_date:
        raise exceptions.InvalidDateWindowException(start_date, end_date)
    
    
    user_id = current_user.user_id
    cat_id, _ = category_service.get_last_cat_id(db, user_id, category)
        
    print("cat_id: {}".format(cat_id))
    print("start_date: {}".format(start_date))
    print("end_date: {}".format(end_date))
    print("min_pri: {}".format(min_pri))
    print("max_pri: {}".format(max_pri))
    
    return {"test": 1}
    
    
    