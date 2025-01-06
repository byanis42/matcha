# services/chat_service/application/settings.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://matcha_user:securepassword@db:5432/matcha_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
