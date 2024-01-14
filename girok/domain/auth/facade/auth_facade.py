from girok.core.authentication.token_manager import TokenManager
from girok.core.exceptions.emitter import raise_custom_exception
from girok.core.utils.auth import check_password
from girok.domain.auth.service.auth_service import AuthService
from girok.domain.exceptions import DomainExceptions
from girok.domain.user.entity.user import User
from girok.domain.user.service.user_service import UserService


class AuthFacade:
    def __init__(self, auth_service: AuthService, user_service: UserService, token_manager: TokenManager):
        self.auth_service = auth_service
        self.user_service = user_service
        self.token_manager = token_manager

    async def send_email_verification_code(self, email: str):
        # Check if email is already registered
        is_user_registered = await self.user_service.is_user_registered_by_email(email=email)
        if is_user_registered:
            raise_custom_exception(DomainExceptions.EMAIL_ALREADY_REGISTERED)

        # Send email verification code
        await self.auth_service.send_email_verification_code(email=email)

    async def verify_email_verification_code(self, email: str, code: str) -> None:
        # Check if email is already registered
        is_user_registered = await self.user_service.is_user_registered_by_email(email=email)
        if is_user_registered:
            raise_custom_exception(DomainExceptions.EMAIL_ALREADY_REGISTERED)

        # Verify email verification code
        await self.auth_service.verify_email_verification_code(email=email, code=code)

    async def register(self, email: str, password: str, verification_code: str):
        # 1. Check if the email is verified
        await self.auth_service.check_email_verified(email=email, verification_code=verification_code)

        # 2. Register user
        await self.user_service.register(user=User(email=email, password=password))

    async def check_email_registered(self, email: str) -> bool:
        return await self.user_service.is_user_registered_by_email(email=email)

    async def login(self, email: str, password: str) -> tuple[str, str]:
        # Check if email is registered
        user = await self.user_service.get_user_or_none_by_email(email=email)
        if not user:
            raise_custom_exception(DomainExceptions.EMAIL_NOT_REGISTERED)

        # Check if password is valid
        stored_hashed_password = user.password
        if not check_password(raw_password=password, hashed_password=stored_hashed_password):
            raise_custom_exception(DomainExceptions.INVALID_PASSWORD)

        # Create JWT Tokens
        assert user.id is not None
        access_token = self.token_manager.create_access_token(sub=user.id)
        refresh_token = self.token_manager.create_refresh_token(sub=user.id)

        return access_token, refresh_token

    async def refresh_token(self, refresh_token: str) -> str:
        return self.token_manager.refresh_token(refresh_token=refresh_token)

    async def send_reset_password_verification_code(self, email: str):
        # Check if email is registered
        is_user_registered = await self.user_service.is_user_registered_by_email(email=email)
        if not is_user_registered:
            raise_custom_exception(DomainExceptions.EMAIL_NOT_REGISTERED)

        # Send email verification code
        await self.auth_service.send_reset_password_email_verification_code(email=email)

    async def verify_reset_password_email_verification_code(self, email: str, code: str) -> None:
        # Check if email is already registered
        is_user_registered = await self.user_service.is_user_registered_by_email(email=email)
        if not is_user_registered:
            raise_custom_exception(DomainExceptions.EMAIL_NOT_REGISTERED)
        # Verify email verification code
        await self.auth_service.verify_reset_password_verification_code(email=email, code=code)

    async def reset_password(self, email: str, new_password: str, verification_code: str):
        # 1. Check if the email is verified
        await self.auth_service.check_reset_password_email_verified(email=email, verification_code=verification_code)

        # 2. Reset password
        await self.user_service.reset_password(email=email, new_password=new_password)

        # 3. Delete reset password email verification
        await self.auth_service.delete_reset_password_email_verification(email=email)
