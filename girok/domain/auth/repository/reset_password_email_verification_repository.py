from dependency_injector.wiring import Provide
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import async_scoped_session

from girok.core.base_class.base_repository import BaseSQLAlchemyRepository
from girok.core.db.transactional import Transactional
from girok.domain.auth.entity import ResetPasswordEmailVerification
from girok.domain.auth.model.reset_password_email_verification import (
    ResetPasswordEmailVerification as ResetPasswordEmailVerificationModel,
)
from girok.domain.auth.repository.mapper.reset_password_email_verification import (
    map_to_reset_password_email_verification,
)

session: async_scoped_session = Provide["session"]


class ResetPasswordEmailVerificationRepository(BaseSQLAlchemyRepository[ResetPasswordEmailVerificationModel]):
    model: type[ResetPasswordEmailVerificationModel]

    def __init__(self, model: type[ResetPasswordEmailVerificationModel]) -> None:
        super().__init__(model)

    @Transactional()
    async def upsert_email_verification(self, email_verification: ResetPasswordEmailVerification) -> None:
        query = select(self.model).where(self.model.email == email_verification.email)
        result = await session.execute(query)
        email_verification_record = result.scalars().first()
        if email_verification_record:
            email_verification_record.verification_code = email_verification.verification_code
            email_verification_record.is_verified = email_verification.is_verified
            email_verification_record.expiration_time = email_verification.expiration_time
        else:
            new_record = self.model(
                email=email_verification.email,
                verification_code=email_verification.verification_code,
                is_verified=email_verification.is_verified,
                expiration_time=email_verification.expiration_time,
            )
            session.add(new_record)

    @Transactional()
    async def get_email_verification_or_none_by_email(self, email: str) -> ResetPasswordEmailVerification | None:
        query = select(self.model).where(self.model.email == email)
        result = await session.execute(query)
        email_verification_record = result.scalars().first()
        if not email_verification_record:
            return None
        return map_to_reset_password_email_verification(email_verification_record=email_verification_record)

    @Transactional()
    async def delete_by_email(self, email: str) -> None:
        query = delete(self.model).where(self.model.email == email)
        await session.execute(query)
