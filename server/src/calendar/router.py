from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.src.database import get_db
import server.src.calendar.schemas as schemas
import server.src.calendar.service as service
import server.src.calendar.exceptions as exceptions

router = APIRouter(
    prefix="/calendar",
    tags=["calendar"]
)

@router.get("/categories", status_code=status.HTTP_200_OK)
async def get_all_categories(db: Session = Depends(get_db)):
    resp = dict()
    # resp = {
    #     "A": {
    #         "B": {
    #             "C": {}
    #         }  
    #     },
    #     "B": {}
    # }
    cats = service.get_subcategories_by_parent_id(db, None)
    for cat in cats:
        resp[cat.name] = service.build_category_tree(db, cat.task_category_id)
    return resp

@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryCreateOut)
async def create_category(
    category: schemas.CategoryCreateIn,
    db: Session = Depends(get_db)
):
    category = category.dict()
    '''
    category = {
        names: HKU or HKU/COMP3230/Assignment
        color: red
    }
    '''
    names = category['names']
    color = category['color']
    parent_id = None
    cumul_path = ""
    for cat_name in names[:-1]:
        cat_id = service.get_category_id_by_name_and_parent_id(db, cat_name, parent_id)
        print(cat_id)
        if not cat_id:
            raise exceptions.SubcategoryNotExistException(cumul_path, cat_name)
        parent_id = cat_id
        cumul_path += cat_name + "/"
        
    new_cat_name = names[-1]
    dup_cat_id = service.get_category_id_by_name_and_parent_id(db, new_cat_name, parent_id)
    if dup_cat_id:
        raise exceptions.CategoryAlreadyExistsException(cumul_path, new_cat_name)
    
    new_cat_data = {
        "name": new_cat_name,
        "super_task_category_id": parent_id,
        "color": color
    }
    new_cat = service.create_category(db, new_cat_data)
    return new_cat
    