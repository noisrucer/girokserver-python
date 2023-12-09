from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from dependency_injector.wiring import Provide
from sqlalchemy.ext.asyncio import async_scoped_session

session: async_scoped_session = Provide["session"]

P = ParamSpec("P")  # Preserving type hints
T = TypeVar("T")


class Transactional:
    def __call__(self, func: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(func)
        async def _transactional(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                result = await func(*args, **kwargs)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

            return result

        return _transactional


# def transaction(func):
#     async def _transaction(*args, **kwargs):
#         try:
#             result = await func(*args, **kwargs)
#             await session.commit()
#         except Exception as e:
#             await session.rollback()
#             raise e
#         return result
#     return _transaction
