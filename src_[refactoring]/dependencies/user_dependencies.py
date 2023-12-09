from fastapi import Depends
from sqlalchemy.orm import Session
from src.config import load_config
from src.domain.user.services import UserService
from src.infrastructure.auth.auth_handler import AuthHandler
from src.infrastructure.database.session import get_db
from src.infrastructure.external_services.email_service.email_sender import EmailSender
from src.persistence.user.repositories import UserRepository

cfg = load_config()


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    user_repository = UserRepository(session=session)
    email_sender = EmailSender(mailgun_api_key=cfg.mailgun.API_KEY, mailgun_domain=cfg.mailgun.DOMAIN)
    auth_handler = AuthHandler(jwt_config=cfg.jwt)
    return UserService(user_repository=user_repository, email_sender=email_sender, auth_handler=auth_handler)
