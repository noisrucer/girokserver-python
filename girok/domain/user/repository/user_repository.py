from dependency_injector.wiring import Provide
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_scoped_session

from girok.core.base_class.base_repository import BaseSQLAlchemyRepository
from girok.core.db.transactional import Transactional
from girok.domain.user.entity.user import User
from girok.domain.user.model.user import User as UserModel
from girok.domain.user.repository.mapper import map_user_entity_to_model

session: async_scoped_session = Provide["session"]


class UserRepository(BaseSQLAlchemyRepository[UserModel]):
    model: type[UserModel]

    def __init__(self, model: type[UserModel]) -> None:
        super().__init__(model)

    async def get_or_none_by_email(self, email: str) -> User:
        query = select(self.model).where(self.model.email == email)
        result = await session.execute(query)
        user = result.scalars().first()
        return user

    @Transactional()
    async def create(self, user: User) -> None:
        user_model = map_user_entity_to_model(user)
        session.add(user_model)

    @Transactional()
    async def update_by_email(self, email: str, params: dict) -> None:
        query = update(self.model).where(self.model.email == email).values(**params)
        await session.execute(query)
