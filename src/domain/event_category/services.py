from src.domain.event_category.entities import EventCategoryEntity
from src.domain.event_category.exceptions import EmptyCategoryPathError
from src.domain.event_category.exceptions import (
    EventCategoryAlreadyExistsError as DomainEventCategoryAlreadyExistsError,
)
from src.domain.event_category.exceptions import (
    EventCategoryNotFoundError as DomainEventCategoryNotFoundError,
)
from src.persistence.event_category.exceptions import (
    EventCategoryAlreadyExistsError as PersistenceEventCategoryAlreadyExistsError,
)
from src.persistence.event_category.exceptions import (
    EventCategoryNotFoundError as PersistenceEventCategoryNotFoundError,
)
from src.persistence.event_category.repositories import EventCategoryRepository


class EventCategoryService:
    def __init__(self, event_category_repository: EventCategoryRepository):
        self.event_category_repository = event_category_repository

    def create_event_category(self, color: str, category_path: list, user_id: int) -> EventCategoryEntity:
        """
        category_path = ["HKU", "COMP3230", "Assignment"]
        """
        parent_category_id = None
        sup_cat_path = "/"
        target_path = category_path[:-1]
        new_category_name = category_path[-1]

        # Get the parent category id of the new category
        for cat_name in target_path:
            try:
                parent_category_id = self.event_category_repository.get_event_category_id_by_name_and_parent_id(
                    parent_event_category_id=parent_category_id, event_category_name=cat_name, user_id=user_id
                )
                sup_cat_path += f"{cat_name}/"
            except PersistenceEventCategoryNotFoundError:
                raise DomainEventCategoryNotFoundError(super_category_path=sup_cat_path, category_name=cat_name)

        # Create the new category
        try:
            new_event_category_entity = self.event_category_repository.create_event_category(
                event_category_entity=EventCategoryEntity(
                    name=new_category_name, color=color, user_id=user_id, parent_event_category_id=parent_category_id
                )
            )
        except PersistenceEventCategoryAlreadyExistsError:
            raise DomainEventCategoryAlreadyExistsError(
                super_category_path=sup_cat_path, category_name=new_category_name
            )
        return new_event_category_entity

    def get_all_categories(self, user_id: int) -> dict[str, dict]:
        top_level_categories = self.event_category_repository.get_category_tree_by_parent_id(user_id=user_id, pid=None)
        result = {}
        for top_category in top_level_categories:
            result[top_category.name] = {
                "subcategories": self._build_category_tree(top_category),
                "color": top_category.color,
            }
        return result

    def delete_event_category(self, path: list[str], user_id: int) -> None:
        if len(path) == 0:
            raise EmptyCategoryPathError(detail="Cannot delete root '/' category")
        cid = self._get_last_cid_from_path(path=path, user_id=user_id)
        self.event_category_repository.delete_event_category_by_id(user_id=user_id, cid=cid)

    def move_event_category(self, path: list[str], new_parent_path: list[str], user_id: int) -> None:
        if len(path) == 0:
            raise EmptyCategoryPathError(detail="Cannot move root '/' category")
        cid = self._get_last_cid_from_path(path=path, user_id=user_id)
        new_pid = self._get_last_cid_from_path(path=new_parent_path, user_id=user_id)

        # Check if new_pid already contains cid
        if self.event_category_repository.check_exist_category_by_cid_and_pid(new_pid, cid, user_id):
            raise DomainEventCategoryAlreadyExistsError(new_parent_path, path[-1])

        self.event_category_repository.move_event_category(cid=cid, pid=new_pid, user_id=user_id)

    def rename_event_category(self, path: list[str], new_name: str, user_id: int) -> None:
        if len(path) == 0:
            raise EmptyCategoryPathError(detail="Cannot rename root '/' category")
        cid = self._get_last_cid_from_path(path=path, user_id=user_id)
        self.event_category_repository.rename_event_category(cid=cid, new_name=new_name, user_id=user_id)

    def _build_category_tree(self, category: EventCategoryEntity) -> dict[str, dict]:
        tree = {}
        for child in category.children:
            tree[child.name] = {"subcategories": self._build_category_tree(child), "color": child.color}
        return tree

    def _get_last_cid_from_path(self, path: list[str], user_id: int) -> int:
        cid = None
        sup_cat_path = "/"
        for cat_name in path:
            try:
                cid = self.event_category_repository.get_event_category_id_by_name_and_parent_id(
                    parent_event_category_id=cid, event_category_name=cat_name, user_id=user_id
                )
                sup_cat_path += f"{cat_name}/"
            except PersistenceEventCategoryNotFoundError:
                raise DomainEventCategoryNotFoundError(super_category_path=sup_cat_path, category_name=cat_name)
        return cid
