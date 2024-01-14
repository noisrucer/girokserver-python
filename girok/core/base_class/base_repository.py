from typing import Generic, TypeVar

from dependency_injector.wiring import Provide
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import async_scoped_session

from girok.core.db.transactional import Transactional

session: async_scoped_session = Provide["session"]


class BaseRepository:
    pass


ModelType = TypeVar("ModelType")


class BaseSQLAlchemyRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_by_id(self, id: int) -> ModelType | None:
        if hasattr(self.model, "id"):
            query = select(self.model).where(self.model.id == id)  # type: ignore
            result = await session.execute(query)
            return result.scalars().first()
        return None

    @Transactional()
    async def delete_by_id(self, id: int) -> None:
        if hasattr(self.model, "id"):
            query = delete(self.model).where(self.model.id == id)  # type: ignore
            await session.execute(query)
        else:
            raise ValueError(f"{self.model} does not have id attribute.")

    @Transactional()
    async def update_by_id(self, id: int, params: dict) -> None:
        if hasattr(self.model, "id"):
            query = update(self.model).where(self.model.id == id).values(**params)  # type: ignore
            await session.execute(query)
        else:
            raise ValueError(f"{self.model} does not have id attribute.")
