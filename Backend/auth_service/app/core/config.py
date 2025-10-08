import os


class Settings:
    def __init__(self) -> None:
        self.database_url: str = os.getenv('DATABASE_URL', '')
        self.jwt_secret: str = os.getenv('JWT_SECRET', 'SECRET_KEY')
        self.jwt_algorithm: str = 'HS256'
        self.jwt_ttl_hours: int = int(os.getenv('JWT_TTL_HOURS', '8'))


settings = Settings()






