import asyncio
from datetime import datetime

from src.domain.exceptions.auth_exceptions import (
    DuplicatedEmailError,
    InvalidVerificationCodeError,
    UserAlreadyVerifiedError,
    UserNotFoundError,
    VerificationCodeExpiredError,
)
from src.domain.user.entities import UserEntity
from src.domain.user.utils import generate_verification_code
from src.infrastructure.auth.crypto_utils import hash_data
from src.infrastructure.external_services.email_service.email_sender import EmailSender
from src.infrastructure.external_services.email_service.utils import (
    read_and_format_html,
)
from src.persistence.user.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository, email_sender: EmailSender):
        self.user_repository = user_repository
        self.email_sender = email_sender

    async def register_user(self, email: str, password: str) -> UserEntity:
        # Check duplicated email
        existing_user = self.user_repository.get_user_by_email(email=email)
        if existing_user:  # TODO: Update user instead of creating new one
            if existing_user.is_verified:
                raise DuplicatedEmailError(email=email)
            else:  # if unverified user exists, delete it and create new one.
                self.user_repository.delete_user_by_id(user_id=existing_user.user_id)

        # Create a new unverified user
        hashed_password = hash_data(raw=password)
        user_entity = UserEntity(email=email, hashed_password=hashed_password, is_verified=False)
        new_user_entity = self.user_repository.create_user(user_entity=user_entity)

        # Send verification email
        verification_code = generate_verification_code()
        content = read_and_format_html(replacements={"__VERIFICATION_CODE__": verification_code})
        asyncio.create_task(
            self.email_sender.send_email(
                recipient=new_user_entity.email, subject="Please verify your email address", content=content
            )
        )

        # Create EmailVerification table entry
        self.user_repository.create_email_verification(
            user_id=new_user_entity.user_id, verification_code=verification_code
        )
        return new_user_entity

    def verify_email(self, email: str, verification_code: str) -> None:
        # Check if user exists
        user_entity = self.user_repository.get_user_by_email(email=email)
        if not user_entity:
            raise UserNotFoundError(email=email)

        # Check if user is already verified
        if user_entity.is_verified:
            raise UserAlreadyVerifiedError(email=email)

        # Check if verification code has expired
        email_verification_entity = self.user_repository.get_email_verification_by_user_id(user_id=user_entity.user_id)
        if email_verification_entity.expiration_time < datetime.utcnow():
            raise VerificationCodeExpiredError(verification_code=verification_code)

        # Check if verification code is correct
        stored_verification_code = email_verification_entity.verification_code
        if verification_code != stored_verification_code:
            raise InvalidVerificationCodeError(verification_code=verification_code)

        # Update user to verified
        user_entity.verify()
        self.user_repository.update_user(user_entity=user_entity, update_fields=["is_verified"])
