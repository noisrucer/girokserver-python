from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv('.env')


class EmailSettings(BaseSettings):
    gmail_sender: str
    gmail_app_password: str
    
    class Config:
        env_file = ".env"
        
        
@lru_cache()
def get_email_settings():
    return EmailSettings()