class EventCategoryEntity:
    def __init__(
        self,
        name: str,
        color: str,
        user_id: int,
        parent_event_category_id: int = None,
        event_category_id: int = None,
        children: list["EventCategoryEntity"] = None,
    ):
        self.name = name
        self.color = color
        self.user_id = user_id
        self.parent_event_category_id = parent_event_category_id
        self.event_category_id = event_category_id
        self.children = children if children is not None else []

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "color": self.color,
            "user_id": self.user_id,
            "parent_event_category_id": self.parent_event_category_id,
            "event_category_id": self.event_category_id,
            "children": self.children,
        }

    def assign_event_category_id(self, event_category_id: int) -> None:
        self.event_category_id = event_category_id
