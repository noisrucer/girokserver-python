from datetime import datetime

from sqlalchemy.orm import Session
from src.domain.user.entities import EmailVerificationEntity, UserEntity
from src.persistence.user.exceptions import InvalidEmailVerificationError
from src.persistence.user.models import EmailVerification, EmailVerificationCode, User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_entity: UserEntity) -> UserEntity:
        new_user_model = User(
            email=user_entity.email, password=user_entity.hashed_password, is_verified=user_entity.is_verified
        )
        self.session.add(new_user_model)
        self.session.commit()
        user_entity.assign_user_id(new_user_model.user_id)
        return user_entity

    def update_user(self, user_entity: UserEntity, update_fields=list[str]) -> UserEntity:
        user_model = self.session.query(User).filter(User.user_id == user_entity.user_id).first()
        if not user_model:
            return None
        for field in update_fields:
            setattr(user_model, field, getattr(user_entity, field))
        self.session.commit()
        return user_entity

    # def create_email_verification(self, user_id: int, verification_code: str) -> None:
    #     email_verification = EmailVerification(user_id=user_id, verification_code=verification_code)
    #     self.session.add(email_verification)
    #     self.session.commit()

    def upsert_email_verification_code(self, email: str, verification_code: str) -> None:
        email_verification_code_model = (
            self.session.query(EmailVerificationCode).filter(EmailVerificationCode.email == email).first()
        )
        if email_verification_code_model:
            email_verification_code_model.verification_code = verification_code
            email_verification_code_model.is_verified = False
        else:
            email_verification_code = EmailVerificationCode(email=email, verification_code=verification_code)
            self.session.add(email_verification_code)
        self.session.commit()

    def verify_email_verification_code(self, email: str, verification_code: str) -> None:
        email_verification_code_model = (
            self.session.query(EmailVerificationCode)
            .filter(EmailVerificationCode.email == email, EmailVerificationCode.verification_code == verification_code)
            .first()
        )

        if not email_verification_code_model:
            raise InvalidEmailVerificationError(
                detail=f"Invalid email verification: either {email} or {verification_code} is incorrect."
            )
        if email_verification_code_model.is_verified:
            raise InvalidEmailVerificationError(detail=f"Invalid email verification: {email} is already verified.")

        if email_verification_code_model.expiration_time < datetime.utcnow():
            raise InvalidEmailVerificationError(detail=f"Invalid email verification: {email} is expired.")
        email_verification_code_model.is_verified = True
        self.session.commit()

    def check_email_verified(self, email: str, verification_code: str) -> None:
        email_verification_code_model = (
            self.session.query(EmailVerificationCode)
            .filter(EmailVerificationCode.email == email, EmailVerificationCode.verification_code == verification_code)
            .first()
        )
        if not email_verification_code_model:
            raise InvalidEmailVerificationError(detail=f"Email not verified: {email} is not yet verified.")
        return email_verification_code_model.is_verified

    def get_user_by_email(self, email: str) -> UserEntity | None:
        user_model = self.session.query(User).filter(User.email == email).first()
        if user_model is None:
            return None
        return UserEntity(
            email=user_model.email,
            hashed_password=user_model.password,
            is_verified=user_model.is_verified,
            user_id=user_model.user_id,
        )

    def get_email_verification_by_user_id(self, user_id: int) -> EmailVerification | None:
        email_verification_model = (
            self.session.query(EmailVerification).filter(EmailVerification.user_id == user_id).first()
        )
        if not email_verification_model:
            return None
        return EmailVerificationEntity(
            user_id=email_verification_model.user_id,
            verification_code=email_verification_model.verification_code,
            expiration_time=email_verification_model.expiration_time,
        )

    def get_verified_user_by_email(self, email: str) -> UserEntity | None:
        user_model = self.session.query(User).filter(User.email == email, User.is_verified is True).first()
        if user_model is None:
            return None
        return UserEntity(
            email=user_model.email, hashed_password=user_model.password, is_verified=True, user_id=user_model.user_id
        )

    def delete_user_by_id(self, user_id: int) -> None:
        user = self.session.query(User).filter(User.user_id == user_id).first()
        self.session.delete(user)
        self.session.commit()

    def is_email_verified(self, email: str) -> bool:
        user_model = self.session.query(User).filter(User.email == email).first()
        if user_model is None:
            return False
        return user_model.is_verified
