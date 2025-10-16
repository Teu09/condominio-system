from typing import List, Optional, Tuple, Dict, Any
from ..core.db import get_conn
import json


def create_tenant(
    name: str, 
    cnpj: str, 
    address: str, 
    phone: str, 
    email: str, 
    theme_config: Optional[Dict[str, Any]] = None
) -> int:
    conn = get_conn()
    cur = conn.cursor()
    try:
        theme_json = json.dumps(theme_config) if theme_config else None
        cur.execute(
            'INSERT INTO tenants (name, cnpj, address, phone, email, theme_config) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            (name, cnpj, address, phone, email, theme_json)
        )
        tenant_id = cur.fetchone()[0]
        conn.commit()
        return tenant_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_tenant_by_id(tenant_id: int) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            'SELECT id, name, cnpj, address, phone, email, theme_config, is_active, created_at FROM tenants WHERE id = %s',
            (tenant_id,)
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def get_tenant_by_cnpj(cnpj: str) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            'SELECT id, name, cnpj, address, phone, email, theme_config, is_active, created_at FROM tenants WHERE cnpj = %s',
            (cnpj,)
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def list_tenants() -> List[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            'SELECT id, name, cnpj, address, phone, email, theme_config, is_active, created_at FROM tenants ORDER BY created_at DESC'
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def update_tenant(
    tenant_id: int,
    name: Optional[str] = None,
    address: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    theme_config: Optional[Dict[str, Any]] = None,
    is_active: Optional[bool] = None
) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    try:
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = %s")
            params.append(name)
        if address is not None:
            updates.append("address = %s")
            params.append(address)
        if phone is not None:
            updates.append("phone = %s")
            params.append(phone)
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if theme_config is not None:
            updates.append("theme_config = %s")
            params.append(json.dumps(theme_config))
        if is_active is not None:
            updates.append("is_active = %s")
            params.append(is_active)
        
        if not updates:
            return False
            
        params.append(tenant_id)
        query = f"UPDATE tenants SET {', '.join(updates)} WHERE id = %s"
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def delete_tenant(tenant_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('UPDATE tenants SET is_active = false WHERE id = %s', (tenant_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
