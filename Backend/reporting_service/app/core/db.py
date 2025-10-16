import psycopg2
from .config import settings


def get_conn():
    return psycopg2.connect(settings.database_url)








