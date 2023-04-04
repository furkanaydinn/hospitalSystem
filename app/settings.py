from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER = os.getenv('POSTGRES_SERVER', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)  # default postgres port is 5432
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'hospital')
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
    #PROJECT_NAME: str = "Hospital Management System"
    #VERSION: str = "0.1.0"
    #API_PREFIX: str = "/api"
    #SECRET_KEY: str = "SECRET_KEY_HERE"
    #ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    #DATABASE_URL: str = "postgresql://postgres:123@localhost:5432/postgres"

settings = Settings()

