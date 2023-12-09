from dependency_injector.wiring import Provide
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session

from girok.core.base_class.base_repository import BaseSQLAlchemyRepository
from girok.core.db.transactional import Transactional  # noqa F401
from girok.domain.category.models import Category

session: async_scoped_session = Provide["session"]


class CategoryRepository(BaseSQLAlchemyRepository[Category]):
    model: type[Category]

    def __init__(self, model: type[Category]) -> None:
        super().__init__(model)

    async def create_category(self, user_id: int, parent_id: int, name: str, color: str) -> Category:
        category = self.model(user_id=user_id, name=name, parent_id=parent_id, color=color)
        session.add(category)
        return category

    async def get_category_by_name_and_parent_id(
        self, parent_id: int | None, cat_name: str, user_id: int
    ) -> Category | None:
        query = select(self.model).filter(
            self.model.user_id == user_id, self.model.parent_id == parent_id, self.model.name == cat_name
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def get_subcategories_by_parent_id(self, user_id: int, pid: int | None) -> list[Category]:
        query = select(self.model).filter(self.model.user_id == user_id, self.model.parent_id == pid)
        result = await session.execute(query)
        return result.scalars().all()
