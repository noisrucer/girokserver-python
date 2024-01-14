from dataclasses import asdict

from dependency_injector import containers, providers
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from girok.config import load_config
from girok.core.authentication.token_manager import TokenManager
from girok.core.db.session_maker import get_session_context
from girok.core.email.email_manager import EmailManager
from girok.core.middlewares.sqlalchemy import SQLAlchemyMiddleware
from girok.domain.auth.container import AuthContainer

# from girok.domain.category.container import CategoryContainer
from girok.domain.user.container import UserContainer


class AppContainer(containers.DeclarativeContainer):
    # Wire the source package
    wiring_config = containers.WiringConfiguration(packages=["girok"], modules=[__name__])

    # configuration: TODO: This is a temporary solution. Optimally, we must use DI to inject config
    cfg = load_config()
    config = providers.Configuration()
    config.from_dict(asdict(cfg))

    # Middlewares
    cors_middleware = providers.Factory(
        Middleware,
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    sqlalchemy_middleware = providers.Factory(Middleware, SQLAlchemyMiddleware)

    middleware_list = providers.List(
        cors_middleware,
        # auth_middleware,
        sqlalchemy_middleware,
    )
    # DB connections
    engine = providers.Factory(
        create_async_engine,
        url=config.db_url,
    )

    async_session_factory = providers.Factory(
        async_sessionmaker,
        bind=engine,
        expire_on_commit=False,
    )

    session = providers.ThreadSafeSingleton(
        async_scoped_session, session_factory=async_session_factory, scopefunc=get_session_context
    )

    # Externals
    token_manager = providers.Factory(
        TokenManager,
        secret_key=config.jwt.secret_key,
        algorithm=config.jwt.algorithm,
        access_token_expire_minutes=config.jwt.access_token_expire_minutes,
        refresh_token_expire_minutes=config.jwt.refresh_token_expire_minutes,
    )

    email_manager = providers.Factory(
        EmailManager, mailgun_api_key=config.mailgun.api_key, mailgun_domain=config.mailgun.domain
    )

    # Domain Containers
    user_container = providers.Container(UserContainer)
    auth_container = providers.Container(
        AuthContainer,
        token_manager=token_manager,
        email_manager=email_manager,
        user_service=user_container.user_service,
    )
    # category_container = providers.Container(CategoryContainer)
