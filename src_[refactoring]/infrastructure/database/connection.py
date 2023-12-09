from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import load_config

cfg = load_config()

MYSQL_DATABASE_URL = (
    f"mysql+pymysql://{cfg.db.MYSQL_USERNAME}:{cfg.db.MYSQL_PASSWORD}@{cfg.db.MYSQL_HOST}:3306/{cfg.db.MYSQL_DB_NAME}"
)
engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
