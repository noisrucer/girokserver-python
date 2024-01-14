from girok.core.exceptions.emitter import raise_custom_exception
from girok.core.utils.auth import hash_password
from girok.domain.exceptions import DomainExceptions
from girok.domain.user.entity.user import User
from girok.domain.user.repository.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_or_none_by_email(self, email: str) -> User:
        return await self.user_repository.get_or_none_by_email(email=email)

    async def is_user_registered_by_email(self, email: str) -> bool:
        user = await self.user_repository.get_or_none_by_email(email)
        return True if user else False

    async def register(self, user: User) -> None:
        # Check if email is already registered
        is_user_registered = await self.is_user_registered_by_email(email=user.email)
        if is_user_registered:
            raise_custom_exception(DomainExceptions.EMAIL_ALREADY_REGISTERED)

        # Hash password
        user.hash_password()

        # Register user
        await self.user_repository.create(user=user)

    async def reset_password(self, email: str, new_password: str) -> None:
        # Hash password
        user = await self.user_repository.get_or_none_by_email(email=email)
        new_hashed_password = hash_password(raw_password=new_password)
        user.password = new_hashed_password

        # Update user
        await self.user_repository.update_by_email(email=email, params={"password": new_hashed_password})
