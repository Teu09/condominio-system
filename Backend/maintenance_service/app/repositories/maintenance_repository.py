from typing import List, Tuple, Optional
from ..core.db import get_conn


def list_maintenance_orders() -> List[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''SELECT id, unit_id, title, description, priority, category, 
                   requested_by, status, expected_date, assigned_to, completed_date, created_at 
                   FROM maintenance_orders ORDER BY created_at DESC''')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_maintenance_order(order_id: int) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''SELECT id, unit_id, title, description, priority, category, 
                   requested_by, status, expected_date, assigned_to, completed_date, created_at 
                   FROM maintenance_orders WHERE id=%s''', (order_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def create_maintenance_order(unit_id: int, title: str, description: str, 
                           priority: str, category: str, requested_by: int, 
                           expected_date=None) -> int:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO maintenance_orders (unit_id, title, description, 
                     priority, category, requested_by, status, expected_date) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id''',
                    (unit_id, title, description, priority, category, 
                     requested_by, 'open', expected_date))
        order_id = cur.fetchone()[0]
        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def update_maintenance_order(order_id: int, status: str = None, 
                           assigned_to: str = None, completed_date=None) -> None:
    conn = get_conn()
    cur = conn.cursor()
    try:
        updates = []
        params = []
        
        if status:
            updates.append('status = %s')
            params.append(status)
        if assigned_to:
            updates.append('assigned_to = %s')
            params.append(assigned_to)
        if completed_date:
            updates.append('completed_date = %s')
            params.append(completed_date)
            
        if updates:
            params.append(order_id)
            query = f"UPDATE maintenance_orders SET {', '.join(updates)} WHERE id = %s"
            cur.execute(query, params)
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def delete_maintenance_order(order_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM maintenance_orders WHERE id=%s', (order_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()




