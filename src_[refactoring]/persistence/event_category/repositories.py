from sqlalchemy.orm import Session
from src.domain.event_category.entities import EventCategoryEntity
from src.persistence.event_category.exceptions import (
    EventCategoryAlreadyExistsError,
    EventCategoryNotFoundError,
)
from src.persistence.event_category.models import EventCategory


class EventCategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_event_category(self, event_category_entity: EventCategoryEntity) -> EventCategoryEntity:
        existing_event_category = (
            self.session.query(EventCategory)
            .filter(
                EventCategory.user_id == event_category_entity.user_id,
                EventCategory.parent_event_category_id == event_category_entity.parent_event_category_id,
                EventCategory.name == event_category_entity.name,
            )
            .first()
        )

        if existing_event_category:
            raise EventCategoryAlreadyExistsError(
                category_name=event_category_entity.name, pid=event_category_entity.parent_event_category_id
            )

        event_category = EventCategory(
            name=event_category_entity.name,
            color=event_category_entity.color,
            user_id=event_category_entity.user_id,
            parent_event_category_id=event_category_entity.parent_event_category_id,
        )

        self.session.add(event_category)
        self.session.commit()
        event_category_entity.assign_event_category_id(event_category.event_category_id)
        return event_category_entity

    def move_event_category(self, cid: int, pid: int | None, user_id: int) -> None:
        category = (
            self.session.query(EventCategory)
            .filter(EventCategory.user_id == user_id, EventCategory.event_category_id == cid)
            .first()
        )
        category.parent_event_category_id = pid
        self.session.commit()

    def rename_event_category(self, cid: int, new_name: str, user_id: int) -> None:
        category = (
            self.session.query(EventCategory)
            .filter(EventCategory.user_id == user_id, EventCategory.event_category_id == cid)
            .first()
        )
        category.name = new_name
        self.session.commit()

    def get_event_category_id_by_name_and_parent_id(
        self, parent_event_category_id: int | None, event_category_name: str, user_id: int
    ) -> int | None:
        event_category = (
            self.session.query(EventCategory)
            .filter(
                EventCategory.user_id == user_id,
                EventCategory.parent_event_category_id == parent_event_category_id,
                EventCategory.name == event_category_name,
            )
            .first()
        )
        if event_category is None:
            raise EventCategoryNotFoundError(category_name=event_category_name, pid=parent_event_category_id)
        return event_category.event_category_id

    def check_exist_category_by_cid_and_pid(self, pid: int | None, cid: int, user_id: int) -> bool:
        event_category = (
            self.session.query(EventCategory)
            .filter(
                EventCategory.user_id == user_id,
                EventCategory.parent_event_category_id == pid,
                EventCategory.event_category_id == cid,
            )
            .first()
        )
        if event_category is None:
            return False
        return True

    def get_category_tree_by_parent_id(self, user_id: int, pid: int | None) -> list[EventCategoryEntity]:
        subcats = (
            self.session.query(EventCategory)
            .filter(EventCategory.user_id == user_id, EventCategory.parent_event_category_id == pid)
            .all()
        )
        subcat_entities = [self._map_to_entity(subcat) for subcat in subcats]
        for subcat_entity in subcat_entities:
            subcat_entity.children = self.get_category_tree_by_parent_id(
                user_id=user_id, pid=subcat_entity.event_category_id
            )
        return subcat_entities

    def delete_event_category_by_id(self, user_id: int, cid: int) -> None:
        print(cid)
        category = (
            self.session.query(EventCategory)
            .filter(EventCategory.user_id == user_id, EventCategory.event_category_id == cid)
            .first()
        )
        self.session.delete(category)
        self.session.commit()

    def _map_to_entity(self, category: EventCategory) -> EventCategoryEntity:
        return EventCategoryEntity(
            name=category.name,
            color=category.color,
            user_id=category.user_id,
            parent_event_category_id=category.parent_event_category_id,
            event_category_id=category.event_category_id,
        )
