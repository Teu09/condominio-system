from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./documents.db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    tenant_id: Optional[int] = None
    upload_path: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    
    class Config:
        env_file = ".env"


settings = Settings()


