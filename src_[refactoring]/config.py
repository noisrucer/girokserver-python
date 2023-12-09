import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class DBConfig:
    MYSQL_HOST: str
    MYSQL_DB_NAME: str
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str


@dataclass
class JWTConfig:
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int


@dataclass
class MailgunConfig:
    DOMAIN: str
    API_KEY: str


@dataclass
class Config:
    db: DBConfig
    jwt: JWTConfig
    mailgun: MailgunConfig


def load_config() -> Config:
    app_env = os.getenv("APP_ENV", "local")
    if app_env == "development":
        load_dotenv(dotenv_path=".env.development")
    elif app_env == "production":
        load_dotenv(dotenv_path=".env.production")
    elif app_env == "local":
        load_dotenv(dotenv_path=".env.local")

    return Config(
        db=DBConfig(
            MYSQL_HOST=os.environ["MYSQL_HOST"],
            MYSQL_DB_NAME=os.environ["MYSQL_DB_NAME"],
            MYSQL_USERNAME=os.environ["MYSQL_USERNAME"],
            MYSQL_PASSWORD=os.environ["MYSQL_PASSWORD"],
        ),
        jwt=JWTConfig(
            SECRET_KEY=os.environ["JWT_SECRET_KEY"],
            ALGORITHM=os.environ["JWT_ALGORITHM"],
            ACCESS_TOKEN_EXPIRE_MINUTES=int(os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]),
            REFRESH_TOKEN_EXPIRE_MINUTES=int(os.environ["JWT_REFRESH_TOKEN_EXPIRE_MINUTES"]),
        ),
        mailgun=MailgunConfig(DOMAIN=os.environ["MAILGUN_DOMAIN"], API_KEY=os.environ["MAILGUN_API_KEY"]),
    )
