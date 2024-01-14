from dependency_injector import containers, providers

from girok.core.authentication.token_manager import TokenManager
from girok.core.email.email_manager import EmailManager
from girok.domain.auth.facade.auth_facade import AuthFacade
from girok.domain.auth.model.email_verification import EmailVerification
from girok.domain.auth.repository.email_verification_repository import (
    EmailVerificationRepository,
)
from girok.domain.auth.service.auth_service import AuthService
from girok.domain.user.service.user_service import UserService


class AuthContainer(containers.DeclarativeContainer):
    email_verification_repository = providers.Factory(EmailVerificationRepository, model=EmailVerification)
    token_manager: providers.Dependency[TokenManager] = providers.Dependency()
    email_manager: providers.Dependency[EmailManager] = providers.Dependency()
    auth_service = providers.Factory(
        AuthService,
        email_verification_repository=email_verification_repository,
        token_manager=token_manager,
        email_manager=email_manager,
    )

    user_service: providers.Dependency[UserService] = providers.Dependency()

    auth_facade = providers.Factory(
        AuthFacade, auth_service=auth_service, user_service=user_service, token_manager=token_manager
    )
