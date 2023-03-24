from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from server.src.config import get_db_settings
db_settings = get_db_settings()

SQLAHCEMY_DATABASE_URL = f"mysql+pymysql://{db_settings.MYSQL_USERNAME}:{db_settings.MYSQL_PASSWORD}@{db_settings.MYSQL_HOST}:3306/{db_settings.MYSQL_DB_NAME}"

engine = create_engine(SQLAHCEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()