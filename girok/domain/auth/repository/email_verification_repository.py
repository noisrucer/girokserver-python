from dependency_injector.wiring import Provide
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session

from girok.core.base_class.base_repository import BaseSQLAlchemyRepository
from girok.core.db.transactional import Transactional
from girok.domain.auth.entity import EmailVerification
from girok.domain.auth.model.email_verification import (
    EmailVerification as EmailVerificationModel,
)
from girok.domain.auth.repository.mapper.email_verification import (
    map_to_email_verification,
)

session: async_scoped_session = Provide["session"]


class EmailVerificationRepository(BaseSQLAlchemyRepository[EmailVerificationModel]):
    model: type[EmailVerificationModel]

    def __init__(self, model: type[EmailVerificationModel]) -> None:
        super().__init__(model)

    @Transactional()
    async def upsert_email_verification(self, email_verification: EmailVerification) -> None:
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
    async def get_email_verification_or_none_by_email(self, email: str) -> EmailVerification | None:
        query = select(self.model).where(self.model.email == email)
        result = await session.execute(query)
        email_verification_record = result.scalars().first()
        if not email_verification_record:
            return None
        return map_to_email_verification(email_verification_record=email_verification_record)
