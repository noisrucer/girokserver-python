from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv('server/.env')
    
class DBSettings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_DB_NAME: str
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    
    class Config:
        env_file = 'server/.env'
        env_file_encoding = 'utf-8'
        
        
@lru_cache()
def get_db_settings():
    return DBSettings()