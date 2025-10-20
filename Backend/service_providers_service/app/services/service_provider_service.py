from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..repositories.service_provider_repository import ServiceProviderRepository
from ..schemas.service_providers import (
    ServiceProviderIn, ServiceProviderOut, ServiceProviderUpdate, 
    ServiceProviderHistoryIn, ServiceProviderHistoryOut, 
    ServiceProviderRatingIn, ServiceProviderRatingOut,
    ServiceProviderSearchIn, ServiceProviderStatsOut
)
from datetime import datetime


class ServiceProviderService:
    def __init__(self, db: Session):
        self.repository = ServiceProviderRepository(db)

    def create_service_provider(self, provider_data: ServiceProviderIn, created_by: str = "Sistema") -> ServiceProviderOut:
        provider = self.repository.create_service_provider(provider_data)
        return ServiceProviderOut.from_orm(provider)

    def get_service_provider(self, provider_id: int) -> Optional[ServiceProviderOut]:
        provider = self.repository.get_service_provider(provider_id)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def get_service_provider_by_cnpj(self, cnpj: str) -> Optional[ServiceProviderOut]:
        provider = self.repository.get_service_provider_by_cnpj(cnpj)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def get_service_provider_by_cpf(self, cpf: str) -> Optional[ServiceProviderOut]:
        provider = self.repository.get_service_provider_by_cpf(cpf)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def get_service_provider_by_email(self, email: str) -> Optional[ServiceProviderOut]:
        provider = self.repository.get_service_provider_by_email(email)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def list_service_providers(self, 
                              status: Optional[str] = None,
                              service_type: Optional[str] = None,
                              is_contractor: Optional[bool] = None,
                              city: Optional[str] = None,
                              state: Optional[str] = None,
                              min_rating: Optional[float] = None,
                              max_rating: Optional[float] = None) -> List[ServiceProviderOut]:
        providers = self.repository.list_service_providers(
            status, service_type, is_contractor, city, state, min_rating, max_rating
        )
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def search_service_providers(self, search_data: ServiceProviderSearchIn) -> List[ServiceProviderOut]:
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def update_service_provider(self, provider_id: int, update_data: ServiceProviderUpdate, changed_by: str = "Sistema") -> Optional[ServiceProviderOut]:
        provider = self.repository.update_service_provider(provider_id, update_data)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def activate_service_provider(self, provider_id: int, activated_by: str) -> Optional[ServiceProviderOut]:
        provider = self.repository.activate_service_provider(provider_id, activated_by)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def deactivate_service_provider(self, provider_id: int, deactivated_by: str) -> Optional[ServiceProviderOut]:
        provider = self.repository.deactivate_service_provider(provider_id, deactivated_by)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def suspend_service_provider(self, provider_id: int, suspended_by: str) -> Optional[ServiceProviderOut]:
        provider = self.repository.suspend_service_provider(provider_id, suspended_by)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def reject_service_provider(self, provider_id: int, rejected_by: str) -> Optional[ServiceProviderOut]:
        provider = self.repository.reject_service_provider(provider_id, rejected_by)
        if provider:
            return ServiceProviderOut.from_orm(provider)
        return None

    def delete_service_provider(self, provider_id: int) -> bool:
        return self.repository.delete_service_provider(provider_id)

    def get_service_provider_history(self, provider_id: int) -> List[ServiceProviderHistoryOut]:
        history = self.repository.get_service_provider_history(provider_id)
        return [ServiceProviderHistoryOut.from_orm(entry) for entry in history]

    def add_service_provider_history(self, history_data: ServiceProviderHistoryIn) -> ServiceProviderHistoryOut:
        history = self.repository.add_service_provider_history(history_data)
        return ServiceProviderHistoryOut.from_orm(history)

    def add_service_provider_rating(self, rating_data: ServiceProviderRatingIn) -> ServiceProviderRatingOut:
        rating = self.repository.add_service_provider_rating(rating_data)
        return ServiceProviderRatingOut.from_orm(rating)

    def get_service_provider_ratings(self, provider_id: int) -> List[ServiceProviderRatingOut]:
        ratings = self.repository.get_service_provider_ratings(provider_id)
        return [ServiceProviderRatingOut.from_orm(rating) for rating in ratings]

    def get_service_providers_by_service_type(self, service_type: str) -> List[ServiceProviderOut]:
        providers = self.repository.get_service_providers_by_service_type(service_type)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_city(self, city: str) -> List[ServiceProviderOut]:
        providers = self.repository.get_service_providers_by_city(city)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_state(self, state: str) -> List[ServiceProviderOut]:
        providers = self.repository.get_service_providers_by_state(state)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_contractors(self) -> List[ServiceProviderOut]:
        providers = self.repository.get_contractors()
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_top_rated_providers(self, limit: int = 10) -> List[ServiceProviderOut]:
        providers = self.repository.get_top_rated_providers(limit)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_recent_providers(self, limit: int = 10) -> List[ServiceProviderOut]:
        providers = self.repository.get_recent_providers(limit)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_provider_stats(self) -> ServiceProviderStatsOut:
        stats = self.repository.get_service_provider_stats()
        return ServiceProviderStatsOut(**stats)

    def get_active_service_providers(self) -> List[ServiceProviderOut]:
        providers = self.repository.list_service_providers(status="active")
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_pending_service_providers(self) -> List[ServiceProviderOut]:
        providers = self.repository.list_service_providers(status="pending")
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_suspended_service_providers(self) -> List[ServiceProviderOut]:
        providers = self.repository.list_service_providers(status="suspended")
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_rejected_service_providers(self) -> List[ServiceProviderOut]:
        providers = self.repository.list_service_providers(status="rejected")
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_rating_range(self, min_rating: float, max_rating: float) -> List[ServiceProviderOut]:
        providers = self.repository.list_service_providers(min_rating=min_rating, max_rating=max_rating)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_contract_status(self, is_contractor: bool) -> List[ServiceProviderOut]:
        providers = self.repository.list_service_providers(is_contractor=is_contractor)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_insurance_expiry(self, days_ahead: int = 30) -> List[ServiceProviderOut]:
        # This would need to be implemented in the repository
        # For now, return all providers
        providers = self.repository.list_service_providers()
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_license_expiry(self, days_ahead: int = 30) -> List[ServiceProviderOut]:
        # This would need to be implemented in the repository
        # For now, return all providers
        providers = self.repository.list_service_providers()
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_contract_expiry(self, days_ahead: int = 30) -> List[ServiceProviderOut]:
        # This would need to be implemented in the repository
        # For now, return all providers
        providers = self.repository.list_service_providers()
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_name(self, name: str) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(name=name)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_company_name(self, company_name: str) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(company_name=company_name)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_phone(self, phone: str) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(phone=phone)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_email(self, email: str) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(email=email)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_cnpj(self, cnpj: str) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(cnpj=cnpj)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_cpf(self, cpf: str) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(cpf=cpf)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_service_types(self, service_types: List[str]) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(service_types=service_types)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_status(self, status: str) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(status=status)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_contractor_status(self, is_contractor: bool) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(is_contractor=is_contractor)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_location(self, city: str, state: str) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(city=city, state=state)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

    def get_service_providers_by_rating(self, min_rating: float, max_rating: float) -> List[ServiceProviderOut]:
        search_data = ServiceProviderSearchIn(min_rating=min_rating, max_rating=max_rating)
        providers = self.repository.search_service_providers(search_data)
        return [ServiceProviderOut.from_orm(provider) for provider in providers]

