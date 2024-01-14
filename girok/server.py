from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from girok.container import AppContainer
from girok.core.db.session_maker import Base
from girok.core.exceptions.base import BaseCustomException

# from girok.domain.auth.views import router as auth_router
# from girok.domain.category.views import router as category_router
# from girok.domain.user.views import router as user_router
from girok.domain.auth.application.auth_controller import router as auth_router


def init_exception_handlers(app: FastAPI) -> None:
    """Initialize exception handlers."""

    @app.exception_handler(Exception)
    def handle_root_exception(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )

    @app.exception_handler(BaseCustomException)
    def handle_custom_exception(request: Request, exc: BaseCustomException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.error_code, "detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    def handle_fastapi_request_exception(request: Request, exc: RequestValidationError) -> JSONResponse:
        err = exc.errors()[0]
        inp = err["input"]
        loc = err["loc"]

        msg = f"Invalid {loc[-1]}: '{inp}' is invalid. {err['msg']}"
        return JSONResponse(
            status_code=400,
            content={"detail": msg},
        )


def init_routers(app: FastAPI) -> None:
    # app.include_router(user_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    # app.include_router(category_router, prefix="/api/v1")


def create_app() -> FastAPI:
    container = AppContainer()
    # TODO: This is a temporary solution. Optimally, we must use DI to inject config
    middleware = container.middleware_list()

    app = FastAPI(
        title="girok server",
        description="girok server",
        version="0.1.0",
        docs_url=None if container.config.env == "prod" else "/docs",
        redoc_url=None if container.config.env == "prod" else "/redoc",
        middleware=middleware,
    )

    init_exception_handlers(app)
    init_routers(app)

    @app.on_event("startup")
    async def startup_event() -> None:
        async with container.engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        await container.engine().dispose()

    return app


app = create_app()
