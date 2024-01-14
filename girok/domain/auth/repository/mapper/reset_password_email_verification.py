from girok.domain.auth.entity import ResetPasswordEmailVerification
from girok.domain.auth.model.reset_password_email_verification import (
    ResetPasswordEmailVerification as ResetPasswordEmailVerificationModel,
)


def map_to_reset_password_email_verification(
    email_verification_record: ResetPasswordEmailVerificationModel,
) -> ResetPasswordEmailVerification:
    return ResetPasswordEmailVerification(
        email=email_verification_record.email,
        verification_code=email_verification_record.verification_code,
        is_verified=email_verification_record.is_verified,
        expiration_time=email_verification_record.expiration_time,
    )
