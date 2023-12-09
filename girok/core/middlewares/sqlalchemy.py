from uuid import uuid4

from dependency_injector.wiring import Provide
from sqlalchemy.ext.asyncio import async_scoped_session
from starlette.types import ASGIApp, Receive, Scope, Send

from girok.core.db.session_maker import reset_session_context, set_session_context

session: async_scoped_session = Provide["session"]


class SQLAlchemyMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())  # UID for each request

        # Create a new session(context) for each request
        context = set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            await session.remove()  # Remove session from context
            reset_session_context(context=context)
