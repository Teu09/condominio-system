from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.service_providers import (
    ServiceProviderIn, ServiceProviderOut, ServiceProviderUpdate, 
    ServiceProviderHistoryIn, ServiceProviderHistoryOut, 
    ServiceProviderRatingIn, ServiceProviderRatingOut,
    ServiceProviderSearchIn, ServiceProviderStatsOut
)
from ..services.service_provider_service import ServiceProviderService

router = APIRouter(prefix="/service-providers", tags=["service-providers"])


@router.post("/", response_model=ServiceProviderOut)
def create_service_provider(provider_data: ServiceProviderIn, created_by: str = "Sistema", db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.create_service_provider(provider_data, created_by)


@router.get("/", response_model=List[ServiceProviderOut])
def list_service_providers(
    status: Optional[str] = None,
    service_type: Optional[str] = None,
    is_contractor: Optional[bool] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    return service.list_service_providers(status, service_type, is_contractor, city, state, min_rating, max_rating)


@router.post("/search", response_model=List[ServiceProviderOut])
def search_service_providers(search_data: ServiceProviderSearchIn, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.search_service_providers(search_data)


@router.get("/{provider_id}", response_model=ServiceProviderOut)
def get_service_provider(provider_id: int, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    provider = service.get_service_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.get("/cnpj/{cnpj}", response_model=ServiceProviderOut)
def get_service_provider_by_cnpj(cnpj: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    provider = service.get_service_provider_by_cnpj(cnpj)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.get("/cpf/{cpf}", response_model=ServiceProviderOut)
def get_service_provider_by_cpf(cpf: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    provider = service.get_service_provider_by_cpf(cpf)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.get("/email/{email}", response_model=ServiceProviderOut)
def get_service_provider_by_email(email: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    provider = service.get_service_provider_by_email(email)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.put("/{provider_id}", response_model=ServiceProviderOut)
def update_service_provider(
    provider_id: int,
    update_data: ServiceProviderUpdate,
    changed_by: str = "Sistema",
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    provider = service.update_service_provider(provider_id, update_data, changed_by)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.post("/{provider_id}/activate", response_model=ServiceProviderOut)
def activate_service_provider(
    provider_id: int,
    activated_by: str,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    provider = service.activate_service_provider(provider_id, activated_by)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.post("/{provider_id}/deactivate", response_model=ServiceProviderOut)
def deactivate_service_provider(
    provider_id: int,
    deactivated_by: str,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    provider = service.deactivate_service_provider(provider_id, deactivated_by)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.post("/{provider_id}/suspend", response_model=ServiceProviderOut)
def suspend_service_provider(
    provider_id: int,
    suspended_by: str,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    provider = service.suspend_service_provider(provider_id, suspended_by)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.post("/{provider_id}/reject", response_model=ServiceProviderOut)
def reject_service_provider(
    provider_id: int,
    rejected_by: str,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    provider = service.reject_service_provider(provider_id, rejected_by)
    if not provider:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return provider


@router.delete("/{provider_id}")
def delete_service_provider(provider_id: int, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    success = service.delete_service_provider(provider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prestador de serviço não encontrado")
    return {"message": "Prestador de serviço excluído com sucesso"}


@router.get("/{provider_id}/history")
def get_service_provider_history(provider_id: int, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_provider_history(provider_id)


@router.post("/{provider_id}/history", response_model=ServiceProviderHistoryOut)
def add_service_provider_history(
    provider_id: int,
    history_data: ServiceProviderHistoryIn,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    history_data.provider_id = provider_id
    return service.add_service_provider_history(history_data)


@router.post("/{provider_id}/ratings", response_model=ServiceProviderRatingOut)
def add_service_provider_rating(
    provider_id: int,
    rating_data: ServiceProviderRatingIn,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    rating_data.provider_id = provider_id
    return service.add_service_provider_rating(rating_data)


@router.get("/{provider_id}/ratings")
def get_service_provider_ratings(provider_id: int, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_provider_ratings(provider_id)


@router.get("/service-type/{service_type}")
def get_service_providers_by_service_type(service_type: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_service_type(service_type)


@router.get("/city/{city}")
def get_service_providers_by_city(city: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_city(city)


@router.get("/state/{state}")
def get_service_providers_by_state(state: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_state(state)


@router.get("/contractors/list")
def get_contractors(db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_contractors()


@router.get("/top-rated/list")
def get_top_rated_providers(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_top_rated_providers(limit)


@router.get("/recent/list")
def get_recent_providers(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_recent_providers(limit)


@router.get("/active/list")
def get_active_service_providers(db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_active_service_providers()


@router.get("/pending/list")
def get_pending_service_providers(db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_pending_service_providers()


@router.get("/suspended/list")
def get_suspended_service_providers(db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_suspended_service_providers()


@router.get("/rejected/list")
def get_rejected_service_providers(db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_rejected_service_providers()


@router.get("/rating-range/list")
def get_service_providers_by_rating_range(
    min_rating: float = Query(0.0, ge=0.0, le=5.0),
    max_rating: float = Query(5.0, ge=0.0, le=5.0),
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_rating_range(min_rating, max_rating)


@router.get("/contract-status/list")
def get_service_providers_by_contract_status(
    is_contractor: bool,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_contract_status(is_contractor)


@router.get("/stats/summary")
def get_service_provider_stats(db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_provider_stats()


@router.get("/search/name/{name}")
def get_service_providers_by_name(name: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_name(name)


@router.get("/search/company/{company_name}")
def get_service_providers_by_company_name(company_name: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_company_name(company_name)


@router.get("/search/phone/{phone}")
def get_service_providers_by_phone(phone: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_phone(phone)


@router.get("/search/email/{email}")
def get_service_providers_by_email(email: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_email(email)


@router.get("/search/cnpj/{cnpj}")
def get_service_providers_by_cnpj(cnpj: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_cnpj(cnpj)


@router.get("/search/cpf/{cpf}")
def get_service_providers_by_cpf(cpf: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_cpf(cpf)


@router.get("/search/service-types/{service_types}")
def get_service_providers_by_service_types(service_types: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    service_types_list = [st.strip() for st in service_types.split(",")]
    return service.get_service_providers_by_service_types(service_types_list)


@router.get("/search/status/{status}")
def get_service_providers_by_status(status: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_status(status)


@router.get("/search/contractor/{is_contractor}")
def get_service_providers_by_contractor_status(is_contractor: bool, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_contractor_status(is_contractor)


@router.get("/search/location/{city}/{state}")
def get_service_providers_by_location(city: str, state: str, db: Session = Depends(get_db)):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_location(city, state)


@router.get("/search/rating/{min_rating}/{max_rating}")
def get_service_providers_by_rating(
    min_rating: float,
    max_rating: float,
    db: Session = Depends(get_db)
):
    service = ServiceProviderService(db)
    return service.get_service_providers_by_rating(min_rating, max_rating)

