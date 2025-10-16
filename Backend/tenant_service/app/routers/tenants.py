from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas.tenants import TenantIn, TenantOut, TenantUpdate
from ..services.tenant_service import tenant_service

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/", response_model=TenantOut)
async def create_tenant(tenant_data: TenantIn):
    try:
        return tenant_service.create_tenant(tenant_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/", response_model=List[TenantOut])
async def list_tenants():
    try:
        return tenant_service.list_tenants()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/{tenant_id}", response_model=TenantOut)
async def get_tenant(tenant_id: int):
    tenant = tenant_service.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")
    return tenant


@router.get("/cnpj/{cnpj}", response_model=TenantOut)
async def get_tenant_by_cnpj(cnpj: str):
    tenant = tenant_service.get_tenant_by_cnpj(cnpj)
    if not tenant:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")
    return tenant


@router.put("/{tenant_id}", response_model=TenantOut)
async def update_tenant(tenant_id: int, update_data: TenantUpdate):
    try:
        tenant = tenant_service.update_tenant(tenant_id, update_data)
        if not tenant:
            raise HTTPException(status_code=404, detail="Condomínio não encontrado")
        return tenant
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.delete("/{tenant_id}")
async def delete_tenant(tenant_id: int):
    success = tenant_service.delete_tenant(tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")
    return {"message": "Condomínio desativado com sucesso"}
