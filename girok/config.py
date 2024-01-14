import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class MySQLConfig:
    host: str
    port: int
    username: str
    password: str
    db_name: str


@dataclass
class JWTConfig:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int


@dataclass
class MailgunConfig:
    api_key: str
    domain: str


@dataclass
class RootConfig:
    env: str
    version: str
    logger_level: str
    db: MySQLConfig
    jwt: JWTConfig
    mailgun: MailgunConfig
    db_url: str


def load_config() -> RootConfig:
    load_dotenv(os.environ["ENV_FILE_PATH"])  # injected in __main__.py

    db_config = MySQLConfig(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        db_name=os.environ["DB_NAME"],
    )

    jwt_config = JWTConfig(
        secret_key=os.environ["JWT_SECRET_KEY"],
        algorithm=os.environ["JWT_ALGORITHM"],
        access_token_expire_minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]),
        refresh_token_expire_minutes=int(os.environ["JWT_REFRESH_TOKEN_EXPIRE_MINUTES"]),
    )

    mailgun_config = MailgunConfig(api_key=os.environ["MAILGUN_API_KEY"], domain=os.environ["MAILGUN_DOMAIN"])

    root_config = RootConfig(
        env=os.environ["ENV"],  # injected in __main__.py
        version="v1",
        logger_level="INFO",
        db=db_config,
        jwt=jwt_config,
        mailgun=mailgun_config,
        db_url=f"mysql+aiomysql://{db_config.username}:{db_config.password}@{db_config.host}:3306/{db_config.db_name}",
    )
    return root_config
