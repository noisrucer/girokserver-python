from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.src.database import get_db
import server.src.category.schemas as schemas
import server.src.category.service as service
import server.src.category.exceptions as exceptions
import server.src.dependencies as glob_dependencies

router = APIRouter(
    prefix="",
    tags=["category"]
)

@router.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(glob_dependencies.get_current_user)]
)
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


@router.post(
    "/categories",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CategoryCreateOut,
    dependencies=[Depends(glob_dependencies.get_current_user)]
)
async def create_category(
    category: schemas.CategoryCreateIn,
    db: Session = Depends(get_db)
):
    category = category.dict()
    '''
    category = {
        names: ['HKU', 'COMP3230', 'Assignment']
        color: red
    }
    '''
    names = category['names']
    color = category['color']
    pid_of_last_cat, cumul_path = service.get_last_cat_id(db, names[:-1])
    new_cat_name = names[-1]
    dup_cat_id = service.get_category_id_by_name_and_parent_id(db, new_cat_name, pid_of_last_cat)
    if dup_cat_id:
        raise exceptions.CategoryAlreadyExistsException(cumul_path, new_cat_name)
    
    new_cat_data = {
        "name": new_cat_name,
        "super_task_category_id": pid_of_last_cat,
        "color": color
    }
    new_cat = service.create_category(db, new_cat_data)
    return new_cat


@router.delete(
    "/categories",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(glob_dependencies.get_current_user)]
)
async def delete_category(category: schemas.CategoryDeleteIn, db: Session=Depends(get_db)):
    '''
    cat_str: ['HKU', 'COMP3230', 'Assignment']
    '''
    category = category.dict()
    cats = category['cats']
    cat_id, _ = service.get_last_cat_id(db, cats)
    service.delete_category(db, cat_id)
        
        
@router.patch(
    "/categories/name",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(glob_dependencies.get_current_user)]
)
async def rename_category(category: schemas.CategoryRenameIn, db: Session=Depends(get_db)):
    category = category.dict()
    cats, new_name = category['cats'], category['new_name']
    # Get cat_id of the original category
    cat_id, _ = service.get_last_cat_id(db, cats)
    
    # Check if new_cats exists (ex. cats[:-1] + /new_cat)
    new_cats = cats[:-1] + [new_name]
    if service.check_exist_category(db, new_cats):
        raise exceptions.CategoryAlreadyExistsException('/'.join(new_cats[:-1]), new_name)
    service.rename_category(db, cat_id, new_name)
    

@router.patch(
    "/categories/parent",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(glob_dependencies.get_current_user)]
)
async def move_category(category: schemas.CategoryMoveIn, db: Session=Depends(get_db)):
    """
    HKU/COMP3230 -> /, /COMP3230 already exist
    """
    category = category.dict()
    cats, new_parent_cats = category['cats'], category['new_parent_cats']
    
    if not cats:
        raise exceptions.CannotMoveRootDirectoryException()
    
    new_cat = new_parent_cats + [cats[-1]]
    if service.check_exist_category(db, new_parent_cats + [cats[-1]]):
        raise exceptions.CategoryAlreadyExistsException('/'.join(new_parent_cats), cats[-1])
        
    cat_id, _ = service.get_last_cat_id(db, cats)
    new_pid, _ = service.get_last_cat_id(db, new_parent_cats)
    if cat_id == new_pid:
        raise exceptions.CannotMoveToSameLocation()
    
    service.move_category(db, cat_id, new_pid)
    