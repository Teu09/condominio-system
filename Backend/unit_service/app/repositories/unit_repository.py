from typing import List, Tuple, Optional
from ..core.db import get_conn


def list_units_rows() -> List[Tuple]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id,block,number,owner_id FROM units ORDER BY id')
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows


def insert_unit(block: str, number: str, owner_id: Optional[int]) -> int:
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute('INSERT INTO units (block,number,owner_id) VALUES (%s,%s,%s) RETURNING id', (block, number, owner_id))
        uid = cur.fetchone()[0]; conn.commit()
        return uid
    except Exception as e:
        conn.rollback(); raise e
    finally:
        cur.close(); conn.close()






