from typing import Union, List
import datetime
from collections import defaultdict

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

import server.src.task.models as models
import server.src.task.exceptions as exceptions
import server.src.category.service as category_service
import server.src.utils as general_utils

def create_task(db: Session, task_data):
    new_task = models.Task(**task_data)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks_by_category(
    db: Session,
    user_id: int,
    cat_ids: List[int],
    start_date: datetime,
    end_date: datetime,
    min_pri: int,
    max_pri: int,
    tag: str
):
    tasks = defaultdict(dict)
    for cat_id in cat_ids:
        cat_name = category_service.get_category_name_by_id(db, cat_id)
        cat_tasks = get_direct_tasks_of_category(
            db=db,
            user_id=user_id,
            cat_id=cat_id,
            start_date=start_date,
            end_date=end_date,
            min_pri=min_pri,
            max_pri=max_pri,
            tag=tag
        )
        sub_cat_ids = category_service.get_subcategory_ids_by_parent_id(db, user_id, cat_id)
        tasks[cat_name]["tasks"] = cat_tasks
        tasks[cat_name]["sub_categories"] = get_tasks_by_category(
            db=db,
            user_id=user_id,
            cat_ids=sub_cat_ids,
            start_date=start_date,
            end_date=end_date,
            min_pri=min_pri,
            max_pri=max_pri,
            tag=tag
        )
    
    return tasks
                
        


def get_tasks(
    db: Session,
    user_id: int,
    cat_ids: Union[List[int], None],
    start_date: datetime,
    end_date: datetime,
    min_pri: int,
    max_pri: int,
    tag: str
):
    tasks_query = db.query(models.Task).\
        filter(
            and_(
                models.Task.user_id == user_id,
                func.date(models.Task.deadline) >= start_date,
                func.date(models.Task.deadline) <= end_date
            )
        )
        
    if tag:
        tasks_query = db.query(models.Task).filter(models.Task.tag == tag)
        
    # Case 1) cat_id == -1 -> ALL categories
    # cat_id == None -> show "none" category
    # cat_id >= 1 -> show selected category
    if cat_ids is not None: # Show selected category tasks
        tasks_query = tasks_query.filter(models.Task.task_category_id.in_(cat_ids))
        
    if min_pri is None and max_pri is None:
        tasks_query = tasks_query.filter(models.Task.priority == None)
    elif min_pri and max_pri:
        tasks_query = tasks_query.filter(
            and_(
                models.Task.priority >= min_pri,
                models.Task.priority <= max_pri   
            )
        )
    else: # only one is None
        raise exceptions.InvalidPriorityPairException()
    
    tasks = tasks_query.order_by(models.Task.deadline.asc()).all()
    return tasks
    

def get_tags(db: Session, user_id: int):
    tags = db.query(models.Task.tag).\
        filter(
            and_(
                models.Task.user_id == user_id,
                models.Task.tag != None
            )    
        ).all()
    tags = {tag[0] for tag in tags} # unique tags
    return list(tags)


def get_direct_tasks_of_category(
    db: Session,
    user_id: int,
    cat_id: int,
    start_date: datetime,
    end_date: datetime,
    min_pri: int,
    max_pri: int,
    tag: str
    ):
    tasks_query = db.query(models.Task).\
        filter(
            and_(
                models.Task.user_id == user_id,
                models.Task.task_category_id == cat_id,
                func.date(models.Task.deadline) >= start_date,
                func.date(models.Task.deadline) <= end_date
            )
        )
        
    if min_pri is None and max_pri is None:
        tasks_query = tasks_query.filter(models.Task.priority == None)
    elif min_pri and max_pri:
        tasks_query = tasks_query.filter(
            and_(
                models.Task.priority >= min_pri,
                models.Task.priority <= max_pri   
            )
        )
    else: # only one is None
        raise exceptions.InvalidPriorityPairException()
    
    if tag:
        tasks_query = tasks_query.filter(models.Task.tag == tag)
    
    tasks = tasks_query.order_by(models.Task.deadline.asc()).all()
    tasks_obj_list = general_utils.sql_obj_list_to_dict_list(tasks)
    return tasks_obj_list
    

