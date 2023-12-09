import asyncio
from datetime import datetime

from src.domain.exceptions.auth_exceptions import (
    DuplicatedEmailError,
    InvalidPasswordError,
    InvalidVerificationCodeError,
    UserAlreadyVerifiedError,
    UserNotFoundError,
    UserNotVerifiedError,
    VerificationCodeExpiredError,
)
from src.domain.user.dtos import LoginUserServiceResponse
from src.domain.user.entities import UserEntity
from src.domain.user.utils import generate_verification_code
from src.infrastructure.auth.auth_handler import AuthHandler
from src.infrastructure.external_services.email_service.email_sender import EmailSender
from src.infrastructure.external_services.email_service.utils import (
    read_and_format_html,
)
from src.persistence.user.exceptions import InvalidEmailVerificationError
from src.persistence.user.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository, email_sender: EmailSender, auth_handler: AuthHandler):
        self.user_repository = user_repository
        self.email_sender = email_sender
        self.auth_handler = auth_handler

    async def send_email_verification_code(self, email: str) -> None:
        # Check if user with this email exists
        user = self.user_repository.get_user_by_email(email=email)
        if user:
            raise DuplicatedEmailError(email=email)

        # Send email verification code. Send verification email
        verification_code = generate_verification_code()
        content = read_and_format_html(replacements={"__VERIFICATION_CODE__": verification_code})
        asyncio.create_task(
            self.email_sender.send_email(recipient=email, subject="Please verify your email address", content=content)
        )

        # Create EmailVerification table entry {email, verification_code, expiration_time, is_verified}
        self.user_repository.upsert_email_verification_code(email=email, verification_code=verification_code)

    def verify_email_verification_code(self, email: str, verification_code: str) -> None:
        self.user_repository.verify_email_verification_code(email=email, verification_code=verification_code)

    def signup(self, email: str, password: str, verification_code: str) -> None:
        # Check if user exists
        user_entity = self.user_repository.get_user_by_email(email=email)
        if user_entity:
            raise DuplicatedEmailError(email=email)

        # Check if verification is complete
        if not self.user_repository.check_email_verified(email=email, verification_code=verification_code):
            raise InvalidEmailVerificationError(detail=f"Email not verified: {email} is not verified.")

        # Create a new user
        hashed_password = self.auth_handler.hash_data(raw=password)
        user_entity = UserEntity(email=email, hashed_password=hashed_password, is_verified=True)
        self.user_repository.create_user(user_entity=user_entity)

    async def register_user(self, email: str, password: str) -> UserEntity:
        # Check duplicated email
        existing_user = self.user_repository.get_user_by_email(email=email)
        if existing_user:  # TODO: Update user instead of creating new one
            if existing_user.is_verified:
                raise DuplicatedEmailError(email=email)
            else:  # if unverified user exists, delete it and create new one.
                self.user_repository.delete_user_by_id(user_id=existing_user.user_id)

        # Create a new unverified user
        hashed_password = self.auth_handler.hash_data(raw=password)
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

    def login_user(self, email: str, password: str) -> LoginUserServiceResponse:
        user_entity = self.user_repository.get_user_by_email(email=email)

        if not user_entity:
            raise UserNotFoundError(email=email)
        if not user_entity.is_verified:
            raise UserNotVerifiedError(email=email)

        stored_hashed_password = user_entity.hashed_password
        if not self.auth_handler.verify_data(raw=password, hashed=stored_hashed_password):
            raise InvalidPasswordError()

        access_token = self.auth_handler.create_access_token(sub=user_entity.user_id)
        refresh_token = self.auth_handler.create_refresh_token(sub=user_entity.user_id)
        return LoginUserServiceResponse(access_token=access_token, refresh_token=refresh_token)

    def refresh_token(self, refresh_token: str) -> str:
        access_token = self.auth_handler.refresh_token(refresh_token=refresh_token)
        return access_token

    def is_email_verified(self, email: str) -> bool:
        return self.user_repository.is_email_verified(email=email)
