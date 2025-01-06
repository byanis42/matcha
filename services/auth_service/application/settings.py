# services/auth_service/application/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    # class Config:
    #     env_file = ".env"  # Cette ligne peut rester commentée si Docker injecte les variables

settings = Settings()
