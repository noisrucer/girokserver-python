from girok.core.db.transactional import Transactional
from girok.domain.category.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
)
from girok.domain.category.models import Category
from girok.domain.category.repository import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repo = category_repository

    @Transactional()
    async def create_category(self, color: str, category_path: list[str], user_id: int) -> Category:
        """
        category_path = ["HKU", "COMP3230", "Assignment"]
        """
        parent_id = None
        sup_cat_path = "/"
        target_path = category_path[:-1]
        new_category_name = category_path[-1]

        # Get the parent category id of the new category
        for cat_name in target_path:
            parent_cat = await self.category_repo.get_category_by_name_and_parent_id(
                parent_id=parent_id, cat_name=cat_name, user_id=user_id
            )
            if parent_cat is None:
                raise CategoryNotFoundError(super_category_path=sup_cat_path, category_name=cat_name)
            parent_id = parent_cat.id
            sup_cat_path += f"{cat_name}/"

        # Check if the new category already exists
        print(parent_id, new_category_name)
        existing_cat = await self.category_repo.get_category_by_name_and_parent_id(
            parent_id=parent_id, cat_name=new_category_name, user_id=user_id
        )
        if existing_cat is not None:
            raise CategoryAlreadyExistsError(super_category_path=sup_cat_path, category_name=new_category_name)

        # Create the new category
        new_category = await self.category_repo.create_category(
            user_id=user_id, parent_id=parent_id, name=new_category_name, color=color
        )
        return new_category

    @Transactional()
    async def get_all_categories(self, user_id: int) -> dict[str, dict]:
        """
        {
            "HKU": {
                "subcategories": {
                    "Assignment": {
                        "subcategories": {},
                        "color": "#83887b"
                    }
                },
                "color": "#83887b"
            },
            "Life": {
                "subcategories": {
                    "A": {
                        "subcategories": {},
                        "color": "#83887b"
                    }
                },
                "color": "#83887b"
            }
        }
        """
        root_categories = await self.category_repo.get_subcategories_by_parent_id(user_id=user_id, pid=None)
        for cat in root_categories:
            print(cat.id, cat.name, await cat.awaitable_attrs.children)
        # print(root_categories)
        # print(root_categories[2].children)
