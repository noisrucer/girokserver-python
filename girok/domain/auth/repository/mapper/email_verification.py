from girok.domain.auth.entity import EmailVerification
from girok.domain.auth.model.email_verification import (
    EmailVerification as EmailVerificationModel,
)


def map_to_email_verification(email_verification_record: EmailVerificationModel) -> EmailVerification:
    return EmailVerification(
        email=email_verification_record.email,
        verification_code=email_verification_record.verification_code,
        is_verified=email_verification_record.is_verified,
        expiration_time=email_verification_record.expiration_time,
    )
