from enum import Enum


class DomainExceptions(Enum):
    # Auth
    EMAIL_ALREADY_REGISTERED = ("EMAIL_ALREADY_REGISTERED", 400, "User already registered")
    EMAIL_NOT_VERIFIED = ("EMAIL_NOT_VERIFIED", 400, "Email not verified")
    EMAIL_VERIFICATION_NOT_FOUND = ("EMAIL_VERIFICATION_NOT_FOUND", 400, "Email verification not found")
    EMAIL_ALREADY_VERIFIED = ("EMAIL_ALREADY_VERIFIED", 400, "Email already verified")
    INVALID_VERIFICATION_CODE = ("INVALID_VERIFICATION_CODE", 400, "Invalid verification code")
    VERIFICATION_CODE_EXPIRED = ("VERIFICATION_CODE_EXPIRED", 400, "Verification code expired")
    EMAIL_NOT_REGISTERED = ("EMAIL_NOT_REGISTERED", 400, "Email not registered")

    # JWT
    INVALID_TOKEN_SCOPE = ("INVALID_TOKEN_SCOPE", 400, "Invalid token scope")
    TOKEN_EXPIRED = ("TOKEN_EXPIRED", 400, "Token is expired")
    INVALID_TOKEN_SIGNATURE = ("INVALID_TOKEN_SIGNATURE", 400, "Invalid token signature")
    INVALID_TOKEN = ("INVALID_TOKEN", 400, "Invalid token")

    INVALID_EMAIL = ("INVALID_EMAIL", 400, "Invalid email")
    INVALID_PASSWORD = ("INVALID_PASSWORD", 400, "Invalid password")
