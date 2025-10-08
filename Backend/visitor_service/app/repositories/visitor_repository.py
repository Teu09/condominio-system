from typing import List, Tuple, Optional
from ..core.db import get_conn


def list_visitors() -> List[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''SELECT id, name, document, unit_id, visit_date, expected_duration, 
                   purpose, contact_phone, status, check_in, check_out 
                   FROM visitors ORDER BY visit_date DESC''')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_visitor(visitor_id: int) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''SELECT id, name, document, unit_id, visit_date, expected_duration, 
                   purpose, contact_phone, status, check_in, check_out 
                   FROM visitors WHERE id=%s''', (visitor_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def create_visitor(name: str, document: str, unit_id: int, visit_date, 
                   expected_duration: int, purpose: str, contact_phone: str = None) -> int:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO visitors (name, document, unit_id, visit_date, 
                     expected_duration, purpose, contact_phone, status) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id''',
                    (name, document, unit_id, visit_date, expected_duration, 
                     purpose, contact_phone, 'scheduled'))
        visitor_id = cur.fetchone()[0]
        conn.commit()
        return visitor_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def update_visitor_status(visitor_id: int, status: str, check_in=None, check_out=None) -> None:
    conn = get_conn()
    cur = conn.cursor()
    try:
        if check_in:
            cur.execute('UPDATE visitors SET status=%s, check_in=%s WHERE id=%s',
                       (status, check_in, visitor_id))
        elif check_out:
            cur.execute('UPDATE visitors SET status=%s, check_out=%s WHERE id=%s',
                       (status, check_out, visitor_id))
        else:
            cur.execute('UPDATE visitors SET status=%s WHERE id=%s',
                       (status, visitor_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def delete_visitor(visitor_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM visitors WHERE id=%s', (visitor_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

