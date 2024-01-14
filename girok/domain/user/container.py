from dependency_injector import containers, providers

from girok.domain.user.model.user import User
from girok.domain.user.repository.user_repository import UserRepository
from girok.domain.user.service.user_service import UserService


class UserContainer(containers.DeclarativeContainer):
    user_repository = providers.Factory(UserRepository, model=User)
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
