from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.shared.exceptions import BaseCustomException


def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


def base_custom_exception_handler(request: Request, exc: BaseCustomException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
