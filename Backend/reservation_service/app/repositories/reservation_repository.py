from typing import List, Tuple, Optional
from ..core.db import get_conn


def list_all() -> List[Tuple]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id,unit_id,area,start_time,end_time,status FROM reservations ORDER BY start_time DESC')
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows


def list_by_owner(owner_id: int) -> List[Tuple]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id,unit_id,area,start_time,end_time,status FROM reservations WHERE unit_id IN (SELECT id FROM units WHERE owner_id=%s) ORDER BY start_time DESC', (owner_id,))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows


def get_unit_owner_id(unit_id: int) -> Optional[int]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT owner_id FROM units WHERE id=%s', (unit_id,))
    rr = cur.fetchone(); cur.close(); conn.close()
    return rr[0] if rr else None


def has_conflict(area: str, start_time, end_time) -> bool:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""SELECT id FROM reservations
                 WHERE area=%s AND status!='cancelled' AND NOT (end_time <= %s OR start_time >= %s)""",
                (area, start_time, end_time))
    conflict = cur.fetchone(); cur.close(); conn.close()
    return bool(conflict)


def count_upcoming_for_unit(unit_id: int) -> int:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""SELECT COUNT(*) FROM reservations WHERE unit_id=%s AND status!='cancelled'
                 AND start_time >= now() AND start_time <= now() + interval '30 days'""",
                (unit_id,))
    cnt = cur.fetchone()[0]; cur.close(); conn.close()
    return cnt


def insert(unit_id: int, area: str, start_time, end_time, status: str) -> int:
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute('INSERT INTO reservations (unit_id, area, start_time, end_time, status) VALUES (%s,%s,%s,%s,%s) RETURNING id', (unit_id, area, start_time, end_time, status))
        rid = cur.fetchone()[0]; conn.commit(); return rid
    except Exception as e:
        conn.rollback(); raise e
    finally:
        cur.close(); conn.close()


def get_unit_id_and_status(res_id: int) -> Optional[Tuple[int, str]]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT unit_id,status FROM reservations WHERE id=%s', (res_id,))
    r = cur.fetchone(); cur.close(); conn.close()
    return (r[0], r[1]) if r else None


def set_status(res_id: int, status: str) -> None:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('UPDATE reservations SET status=%s WHERE id=%s', (status, res_id))
    conn.commit(); cur.close(); conn.close()



















