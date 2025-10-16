import datetime
import jwt
import json
from fastapi import HTTPException
from ..core.config import settings
from ..repositories.user_repository import get_user_by_email, get_tenant_by_id, get_super_admin_by_email


def authenticate(email: str, password: str, tenant_id: int | None = None) -> dict:
    row = get_user_by_email(email, tenant_id)
    if not row:
        raise HTTPException(status_code=401, detail='Credenciais inválidas')
    
    user_id, user_tenant_id, user_password, role, full_name, permissions_json, is_active = row
    
    if user_password != password or not is_active:
        raise HTTPException(status_code=401, detail='Credenciais inválidas')
    
    # Verificar se o tenant está ativo
    tenant_row = get_tenant_by_id(user_tenant_id)
    if not tenant_row:
        raise HTTPException(status_code=401, detail='Condomínio não encontrado ou inativo')
    
    tenant_id, tenant_name, tenant_cnpj, tenant_theme_config = tenant_row
    
    # Parse permissions
    permissions = []
    if permissions_json:
        try:
            permissions = json.loads(permissions_json)
        except json.JSONDecodeError:
            permissions = []
    
    payload = {
        'sub': str(user_id),
        'tenant_id': user_tenant_id,
        'role': role,
        'permissions': permissions,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=settings.jwt_ttl_hours),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    
    # Parse theme config
    theme_config = None
    if tenant_theme_config:
        try:
            theme_config = json.loads(tenant_theme_config)
        except json.JSONDecodeError:
            theme_config = None
    
    return {
        'access_token': token,
        'token_type': 'bearer',
        'user': {
            'id': user_id, 
            'tenant_id': user_tenant_id,
            'email': email, 
            'full_name': full_name, 
            'role': role,
            'permissions': permissions,
            'is_active': is_active
        },
        'tenant': {
            'id': tenant_id,
            'name': tenant_name,
            'cnpj': tenant_cnpj,
            'theme_config': theme_config
        }
    }


def authenticate_super_admin(email: str, password: str) -> dict:
    """Autenticação específica para super administrador"""
    row = get_super_admin_by_email(email)
    if not row:
        raise HTTPException(status_code=401, detail='Credenciais de super admin inválidas')
    
    user_id, user_tenant_id, user_password, role, full_name, permissions_json, is_active = row
    
    if user_password != password or not is_active:
        raise HTTPException(status_code=401, detail='Credenciais de super admin inválidas')
    
    # Parse permissions
    permissions = []
    if permissions_json:
        try:
            permissions = json.loads(permissions_json)
        except json.JSONDecodeError:
            permissions = []
    
    payload = {
        'sub': str(user_id),
        'tenant_id': None,  # Super admin não tem tenant específico
        'role': role,
        'permissions': permissions,
        'is_super_admin': True,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=settings.jwt_ttl_hours),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    
    return {
        'access_token': token,
        'token_type': 'bearer',
        'user': {
            'id': user_id, 
            'tenant_id': None,
            'email': email, 
            'full_name': full_name, 
            'role': role,
            'permissions': permissions,
            'is_active': is_active,
            'is_super_admin': True
        },
        'tenant': None  # Super admin não tem tenant específico
    }






