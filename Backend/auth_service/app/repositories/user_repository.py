from typing import Optional, Tuple
from ..core.db import get_conn


def get_user_by_email(email: str) -> Optional[Tuple[int, str, str, str]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, password, role, full_name FROM users WHERE email=%s', (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row



