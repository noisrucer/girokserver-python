from dependency_injector.wiring import Provide
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session

from girok.core.base_class.base_repository import BaseSQLAlchemyRepository
from girok.core.db.transactional import Transactional
from girok.domain.user.models import EmailVerification, User

session: async_scoped_session = Provide["session"]


class UserRepository(BaseSQLAlchemyRepository[User]):
    model: type[User]

    def __init__(self, model: type[User]) -> None:
        super().__init__(model)

    @Transactional()
    async def get_user_by_email(self, email: str) -> User | None:
        query = select(self.model).filter(self.model.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @Transactional()
    async def create_user(self, email: str, hashed_password: str) -> User:
        user = self.model(email=email, password=hashed_password)
        session.add(user)
        return user


class EmailVerificationRepository(BaseSQLAlchemyRepository[EmailVerification]):
    model: type[EmailVerification]

    def __init__(self, model: type[EmailVerification]) -> None:
        super().__init__(model)

    @Transactional()
    async def create_email_verification(self, user_id: int, verification_code: str) -> None:
        email_verification = self.model(user_id=user_id, verification_code=verification_code)
        session.add(email_verification)

    @Transactional()
    async def get_email_verification_by_user_id(self, user_id: int) -> EmailVerification | None:
        query = select(self.model).filter(self.model.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().first()
