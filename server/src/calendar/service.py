from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_

import server.src.calendar.models as models

def create_category(db: Session, cat_data):
    new_cat = models.TaskCategory(**cat_data)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat


def check_exist_category(db: Session, name: str):
    category = db.query(models.TaskCategory).\
        filter(models.TaskCategory.name == name).\
        first()
    return category


def get_category_id_by_name_and_parent_id(db: Session, name: str, parent_id: int):
    category = db.query(models.TaskCategory.task_category_id).\
        filter(
            and_(
                models.TaskCategory.name == name,
                models.TaskCategory.super_task_category_id == parent_id
            )
        ).first()
    if not category:
        return None
    return category[0]


def get_category_name_by_id(db: Session, cat_id: int):
    cat = db.query(models.TaskCategory.name).\
        filter(models.TaskCategory.task_category_id == cat_id).\
        first()
    return cat_id[0] if cat else None


def get_subcategories_by_parent_id(db: Session, pid: int):
    subcats = db.query(models.TaskCategory).\
        filter(models.TaskCategory.super_task_category_id == pid).\
        all()
    return subcats


def build_category_tree(db: Session, cat_id):
    subs = get_subcategories_by_parent_id(db, cat_id)
    if subs is None: # Base case
        return {}
    res = dict()
    for sub in subs:
        res[sub.name] = build_category_tree(db, sub.task_category_id)
    return res


def is_super_category(db: Session, super: str, sub: str):
    sub_cat = db.query(models.TaskCategory).\
        filter(
            and_(
                models.TaskCategory.name == sub,
                models.TaskCategory.super_category_name == super
            )
        ).first()
    return sub_cat

