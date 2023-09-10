from collections import defaultdict

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import src.category.constants as category_constants
import src.category.exceptions as exceptions
import src.category.schemas as schemas
import src.category.service as service
import src.dependencies as glob_dependencies
import src.user.models as user_models
from src.database import get_db

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_categories(
    db: Session = Depends(get_db), current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    user_id = current_user.user_id
    resp = defaultdict(dict)
    cats = service.get_subcategories_by_parent_id(db, user_id=user_id, pid=None)
    for cat in cats:
        resp[cat.name]["subcategories"] = service.build_category_tree(db, user_id, cat.task_category_id)
        resp[cat.name]["color"] = cat.color

    resp["No Category"] = {"color": "grey", "subcategories": {}}

    return resp


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryCreateOut)
async def create_category(
    category: schemas.CategoryCreateIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    category = category.dict()
    """ Example
    category = {
        names: ['HKU', 'COMP3230', 'Assignment']
        color: yellow
    }
    """
    names = category["names"]
    color = category["color"]
    if color and color not in category_constants.CATEGORY_COLORS:
        raise exceptions.CategoryColorNotExistException(color)

    user_id = current_user.user_id

    pid_of_second_last_cat, cumul_path = service.get_last_cat_id(db, user_id, names[:-1])

    # If given, check if the subdirectory color is equal to the parent's color,
    if color is None:
        if pid_of_second_last_cat is not None:
            color = service.get_category_color_by_id(db, user_id, pid_of_second_last_cat)  # set to parent's color
        else:
            # Select non-overlapping colors
            existing_colors = set(service.get_all_category_colors(db, user_id).values())
            for c in category_constants.CATEGORY_COLORS:  # Assign color (lower index higher priority)
                if c in existing_colors:
                    continue
                color = c
                break
            if color is None:  # If no available non-overlapping color, assign the default color
                color = category_constants.DEFAULT_CATEGORY_COLOR
    else:
        if pid_of_second_last_cat is not None:
            parent_color = service.get_category_color_by_id(db, user_id, pid_of_second_last_cat)
            if color != parent_color:
                raise exceptions.CategoryColorException(names[-1], color, "/".join(names[:-1]), parent_color)

    new_cat_name = names[-1]
    dup_cat_id = service.get_category_id_by_name_and_parent_id(db, user_id, new_cat_name, pid_of_second_last_cat)
    if dup_cat_id:
        raise exceptions.CategoryAlreadyExistsException(cumul_path, new_cat_name)

    new_cat_data = {
        "user_id": user_id,
        "name": new_cat_name,
        "super_task_category_id": pid_of_second_last_cat,
        "color": color,
    }
    new_cat = service.create_category(db, new_cat_data)
    return new_cat


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category: schemas.CategoryDeleteIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    category = category.dict()
    cats = category["cats"]
    user_id = current_user.user_id
    cat_id, _ = service.get_last_cat_id(db, user_id, cats)
    service.delete_category(db, user_id, cat_id)


@router.patch("/name", status_code=status.HTTP_204_NO_CONTENT)
async def rename_category(
    category: schemas.CategoryRenameIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    category = category.dict()
    (
        cats,
        new_name,
    ) = (
        category["cats"],
        category["new_name"],
    )
    user_id = current_user.user_id

    # Get cat_id of the original category
    cat_id, _ = service.get_last_cat_id(db, user_id, cats)

    # Check if new_cats exists (ex. cats[:-1] + /new_cat)
    new_cats = cats[:-1] + [new_name]
    if service.check_exist_category(db, user_id, new_cats):
        raise exceptions.CategoryAlreadyExistsException("/".join(new_cats[:-1]), new_name)
    service.rename_category(db, user_id, cat_id, new_name)


@router.patch("/parent", status_code=status.HTTP_200_OK)
async def move_category(
    category: schemas.CategoryMoveIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    """
    cats: ['HKU', 'COMP3230']
    new_parent_cats: ['Dev', 'Git']

    Then, we want to move the entire HKU/COMP3230 category into under Dev/Git category.
    """
    category = category.dict()
    cats, new_parent_cats = category["cats"], category["new_parent_cats"]
    user_id = current_user.user_id
    if not cats:
        raise exceptions.CannotMoveRootDirectoryException()

    new_parent_cats + [cats[-1]]

    if service.check_exist_category(db, user_id, new_parent_cats + [cats[-1]]):
        raise exceptions.CategoryAlreadyExistsException("/".join(new_parent_cats), cats[-1])

    cat_id, _ = service.get_last_cat_id(db, user_id, cats)
    new_pid, _ = service.get_last_cat_id(db, user_id, new_parent_cats)
    if cat_id == new_pid:
        raise exceptions.CannotMoveToSameLocation()

    service.move_category(db, user_id, cat_id, new_pid)


@router.get("/last-cat-id", status_code=status.HTTP_200_OK)
def get_last_cat_id(
    cat_data: schemas.LastCategoryIdIn,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    cat_data = cat_data.dict()
    user_id = current_user.user_id
    cat_id, _ = service.get_last_cat_id(db, user_id, cat_data["cats"])
    return {"cat_id": cat_id}


@router.get("/{cat_id}/color", status_code=status.HTTP_200_OK)
def get_category_color(
    cat_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(glob_dependencies.get_current_user),
):
    user_id = current_user.user_id
    color = service.get_category_color_by_id(db, user_id, cat_id)
    return {"color": color}


@router.get("/color", status_code=status.HTTP_200_OK)
def get_category_colors_dict(
    db: Session = Depends(get_db), current_user: user_models.User = Depends(glob_dependencies.get_current_user)
):
    user_id = current_user.user_id
    colors = service.get_all_category_colors(db, user_id)
    colors["No Category"] = "grey"
    return colors
