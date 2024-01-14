from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.shared.exceptions import BaseCustomException


def pydantic_validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.errors()})


def base_custom_exception_handler(request: Request, exc: BaseCustomException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": f"{exc}"})


def fastapi_request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()[0]["msg"]})


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
    app.add_exception_handler(BaseCustomException, base_custom_exception_handler)
    app.add_exception_handler(RequestValidationError, fastapi_request_validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
