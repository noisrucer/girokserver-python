from girok.core.exceptions.base import BaseCustomException
from girok.domain.exceptions import DomainExceptions


def raise_custom_exception(exc: DomainExceptions) -> None:
    error_code, status_code, error_msg = exc.value

    raise BaseCustomException(error_code=error_code, status_code=status_code, detail=error_msg)
