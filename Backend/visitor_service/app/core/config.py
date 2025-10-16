import os


class Settings:
    def __init__(self) -> None:
        self.database_url: str = os.getenv('DATABASE_URL', '')


settings = Settings()








