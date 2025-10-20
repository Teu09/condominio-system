from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./events.db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    tenant_id: Optional[int] = None
    
    class Config:
        env_file = ".env"


settings = Settings()


