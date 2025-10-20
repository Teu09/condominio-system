from typing import Optional, Tuple
from ..core.db import get_conn
import json


def get_user_by_email(email: str, tenant_id: Optional[int] = None) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    if tenant_id is not None:
        cur.execute(
            'SELECT id, tenant_id, password, role, full_name, permissions, is_active FROM users WHERE email=%s AND tenant_id=%s',
            (email, tenant_id)
        )
    else:
        cur.execute(
            'SELECT id, tenant_id, password, role, full_name, permissions, is_active FROM users WHERE email=%s',
            (email,)
        )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_super_admin_by_email(email: str) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'SELECT id, tenant_id, password, role, full_name, permissions, is_active FROM users WHERE email=%s AND role=%s',
        (email, 'super_admin')
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_tenant_by_id(tenant_id: int) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'SELECT id, name, cnpj, theme_config FROM tenants WHERE id=%s AND is_active=true',
        (tenant_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row






