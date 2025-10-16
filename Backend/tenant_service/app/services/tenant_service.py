from typing import List, Optional, Dict, Any
from ..repositories.tenant_repository import (
    create_tenant, get_tenant_by_id, get_tenant_by_cnpj, 
    list_tenants, update_tenant, delete_tenant
)
from ..schemas.tenants import TenantIn, TenantOut, TenantUpdate, TenantThemeConfig
from datetime import datetime
import json
import psycopg2
from ..core.config import settings


class TenantService:
    def create_tenant(self, tenant_data: TenantIn) -> TenantOut:
        # Verificar se CNPJ já existe
        existing = get_tenant_by_cnpj(tenant_data.cnpj)
        if existing:
            raise ValueError("CNPJ já cadastrado")
        
        # Preparar configuração de tema
        theme_config = None
        if tenant_data.theme_config:
            theme_config = tenant_data.theme_config.dict()
        
        # Criar tenant
        tenant_id = create_tenant(
            name=tenant_data.name,
            cnpj=tenant_data.cnpj,
            address=tenant_data.address,
            phone=tenant_data.phone,
            email=tenant_data.email,
            theme_config=theme_config
        )
        
        # Criar usuário administrador
        self._create_admin_user(tenant_id, tenant_data.admin_email, tenant_data.admin_password, tenant_data.admin_name)
        
        # Retornar tenant criado
        tenant = get_tenant_by_id(tenant_id)
        return self._row_to_tenant_out(tenant)
    
    def _create_admin_user(self, tenant_id: int, email: str, password: str, full_name: str):
        """Cria o usuário administrador para o tenant"""
        conn = psycopg2.connect(settings.database_url)
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO users (tenant_id, email, password, full_name, role, permissions) VALUES (%s, %s, %s, %s, %s, %s)',
                (tenant_id, email, password, full_name, 'admin', json.dumps(['all']))
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
    
    def get_tenant(self, tenant_id: int) -> Optional[TenantOut]:
        tenant = get_tenant_by_id(tenant_id)
        if not tenant:
            return None
        return self._row_to_tenant_out(tenant)
    
    def get_tenant_by_cnpj(self, cnpj: str) -> Optional[TenantOut]:
        tenant = get_tenant_by_cnpj(cnpj)
        if not tenant:
            return None
        return self._row_to_tenant_out(tenant)
    
    def list_tenants(self) -> List[TenantOut]:
        tenants = list_tenants()
        return [self._row_to_tenant_out(tenant) for tenant in tenants]
    
    def update_tenant(self, tenant_id: int, update_data: TenantUpdate) -> Optional[TenantOut]:
        # Preparar dados para atualização
        update_dict = update_data.dict(exclude_unset=True)
        
        # Converter theme_config se presente
        if 'theme_config' in update_dict and update_dict['theme_config']:
            update_dict['theme_config'] = update_dict['theme_config'].dict()
        
        # Atualizar tenant
        success = update_tenant(tenant_id, **update_dict)
        if not success:
            return None
        
        # Retornar tenant atualizado
        return self.get_tenant(tenant_id)
    
    def delete_tenant(self, tenant_id: int) -> bool:
        return delete_tenant(tenant_id)
    
    def _row_to_tenant_out(self, row: tuple) -> TenantOut:
        tenant_id, name, cnpj, address, phone, email, theme_config_json, is_active, created_at = row
        
        theme_config = None
        if theme_config_json:
            try:
                theme_config = json.loads(theme_config_json)
            except json.JSONDecodeError:
                theme_config = None
        
        return TenantOut(
            id=tenant_id,
            name=name,
            cnpj=cnpj,
            address=address,
            phone=phone,
            email=email,
            theme_config=theme_config,
            is_active=is_active,
            created_at=created_at
        )


tenant_service = TenantService()
