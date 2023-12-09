from email_validator import EmailNotValidError, validate_email


def is_valid_email_format(email: str) -> bool:
    try:
        _ = validate_email(email)
    except EmailNotValidError:
        return False
    return True
