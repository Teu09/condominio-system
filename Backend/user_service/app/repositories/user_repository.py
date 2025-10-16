from typing import List, Optional, Tuple
from ..core.db import get_conn
import json


def list_users_rows(tenant_id: int) -> List[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            'SELECT id, tenant_id, email, full_name, role, permissions, is_active FROM users WHERE tenant_id=%s ORDER BY id DESC',
            (tenant_id,)
        )
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()


def insert_user(tenant_id: int, email: str, password: str, full_name: Optional[str], role: str, permissions: Optional[List[str]] = None) -> int:
    conn = get_conn()
    cur = conn.cursor()
    try:
        permissions_json = json.dumps(permissions or [])
        cur.execute(
            'INSERT INTO users (tenant_id, email, password, full_name, role, permissions) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            (tenant_id, email, password, full_name, role, permissions_json)
        )
        uid = cur.fetchone()[0]
        conn.commit()
        return uid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_user_row(user_id: int, tenant_id: int) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            'SELECT id, tenant_id, email, full_name, role, permissions, is_active FROM users WHERE id=%s AND tenant_id=%s',
            (user_id, tenant_id)
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def update_user(user_id: int, tenant_id: int, full_name: Optional[str] = None, role: Optional[str] = None, permissions: Optional[List[str]] = None, is_active: Optional[bool] = None) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    try:
        updates = []
        params = []
        
        if full_name is not None:
            updates.append("full_name = %s")
            params.append(full_name)
        if role is not None:
            updates.append("role = %s")
            params.append(role)
        if permissions is not None:
            updates.append("permissions = %s")
            params.append(json.dumps(permissions))
        if is_active is not None:
            updates.append("is_active = %s")
            params.append(is_active)
        
        if not updates:
            return False
            
        params.extend([user_id, tenant_id])
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s AND tenant_id = %s"
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def delete_user(user_id: int, tenant_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('UPDATE users SET is_active = false WHERE id = %s AND tenant_id = %s', (user_id, tenant_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()













