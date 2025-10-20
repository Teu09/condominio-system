from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./minutes.db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    tenant_id: Optional[int] = None
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()


