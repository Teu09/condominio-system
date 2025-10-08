from typing import List, Optional, Tuple
from ..core.db import get_conn


def list_users_rows() -> List[Tuple]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id,email,full_name,role FROM users ORDER BY id DESC')
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows


def insert_user(email: str, password: str, full_name: Optional[str], role: str) -> int:
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (email,password,full_name,role) VALUES (%s,%s,%s,%s) RETURNING id', (email,password,full_name,role))
        uid = cur.fetchone()[0]; conn.commit()
        return uid
    except Exception as e:
        conn.rollback(); raise e
    finally:
        cur.close(); conn.close()


def get_user_row(user_id: int) -> Optional[Tuple]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id,email,full_name,role FROM users WHERE id=%s', (user_id,))
    r = cur.fetchone(); cur.close(); conn.close()
    return r






