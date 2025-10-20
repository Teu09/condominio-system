from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from ..models.service_providers import ServiceProvider, ServiceProviderHistory, ServiceProviderRating
from ..schemas.service_providers import ServiceProviderIn, ServiceProviderUpdate, ServiceProviderHistoryIn, ServiceProviderRatingIn, ServiceProviderSearchIn
from datetime import datetime, date


class ServiceProviderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_service_provider(self, provider_data: ServiceProviderIn) -> ServiceProvider:
        db_provider = ServiceProvider(
            name=provider_data.name,
            company_name=provider_data.company_name,
            cnpj=provider_data.cnpj,
            cpf=provider_data.cpf,
            email=provider_data.email,
            phone=provider_data.phone,
            address=provider_data.address,
            city=provider_data.city,
            state=provider_data.state,
            zip_code=provider_data.zip_code,
            service_types=provider_data.service_types,
            description=provider_data.description,
            hourly_rate=provider_data.hourly_rate,
            daily_rate=provider_data.daily_rate,
            monthly_rate=provider_data.monthly_rate,
            is_contractor=provider_data.is_contractor,
            contract_start_date=provider_data.contract_start_date,
            contract_end_date=provider_data.contract_end_date,
            insurance_number=provider_data.insurance_number,
            insurance_expiry=provider_data.insurance_expiry,
            license_number=provider_data.license_number,
            license_expiry=provider_data.license_expiry,
            rating=provider_data.rating,
            notes=provider_data.notes,
            created_by=provider_data.created_by
        )
        
        self.db.add(db_provider)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = ServiceProviderHistory(
            provider_id=db_provider.id,
            action="created",
            description="Prestador de serviço criado",
            changed_by=provider_data.created_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def get_service_provider(self, provider_id: int) -> Optional[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(ServiceProvider.id == provider_id).first()

    def get_service_provider_by_cnpj(self, cnpj: str) -> Optional[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(ServiceProvider.cnpj == cnpj).first()

    def get_service_provider_by_cpf(self, cpf: str) -> Optional[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(ServiceProvider.cpf == cpf).first()

    def get_service_provider_by_email(self, email: str) -> Optional[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(ServiceProvider.email == email).first()

    def list_service_providers(self, 
                              status: Optional[str] = None,
                              service_type: Optional[str] = None,
                              is_contractor: Optional[bool] = None,
                              city: Optional[str] = None,
                              state: Optional[str] = None,
                              min_rating: Optional[float] = None,
                              max_rating: Optional[float] = None) -> List[ServiceProvider]:
        query = self.db.query(ServiceProvider)
        
        if status:
            query = query.filter(ServiceProvider.status == status)
        if service_type:
            query = query.filter(ServiceProvider.service_types.contains([service_type]))
        if is_contractor is not None:
            query = query.filter(ServiceProvider.is_contractor == is_contractor)
        if city:
            query = query.filter(ServiceProvider.city.ilike(f"%{city}%"))
        if state:
            query = query.filter(ServiceProvider.state == state)
        if min_rating is not None:
            query = query.filter(ServiceProvider.rating >= min_rating)
        if max_rating is not None:
            query = query.filter(ServiceProvider.rating <= max_rating)
            
        return query.order_by(desc(ServiceProvider.created_at)).all()

    def search_service_providers(self, search_data: ServiceProviderSearchIn) -> List[ServiceProvider]:
        query = self.db.query(ServiceProvider)
        
        if search_data.name:
            query = query.filter(ServiceProvider.name.ilike(f"%{search_data.name}%"))
        if search_data.company_name:
            query = query.filter(ServiceProvider.company_name.ilike(f"%{search_data.company_name}%"))
        if search_data.cnpj:
            query = query.filter(ServiceProvider.cnpj == search_data.cnpj)
        if search_data.email:
            query = query.filter(ServiceProvider.email.ilike(f"%{search_data.email}%"))
        if search_data.phone:
            query = query.filter(ServiceProvider.phone.ilike(f"%{search_data.phone}%"))
        if search_data.service_types:
            for service_type in search_data.service_types:
                query = query.filter(ServiceProvider.service_types.contains([service_type]))
        if search_data.status:
            query = query.filter(ServiceProvider.status == search_data.status)
        if search_data.is_contractor is not None:
            query = query.filter(ServiceProvider.is_contractor == search_data.is_contractor)
        if search_data.city:
            query = query.filter(ServiceProvider.city.ilike(f"%{search_data.city}%"))
        if search_data.state:
            query = query.filter(ServiceProvider.state == search_data.state)
        if search_data.min_rating is not None:
            query = query.filter(ServiceProvider.rating >= search_data.min_rating)
        if search_data.max_rating is not None:
            query = query.filter(ServiceProvider.rating <= search_data.max_rating)
            
        return query.order_by(desc(ServiceProvider.rating), desc(ServiceProvider.created_at)).all()

    def update_service_provider(self, provider_id: int, update_data: ServiceProviderUpdate) -> Optional[ServiceProvider]:
        db_provider = self.get_service_provider(provider_id)
        if not db_provider:
            return None
        
        # Store old values for history
        old_values = {
            "name": db_provider.name,
            "company_name": db_provider.company_name,
            "email": db_provider.email,
            "phone": db_provider.phone,
            "status": db_provider.status
        }
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_provider, field, value)
        
        db_provider.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "name": db_provider.name,
            "company_name": db_provider.company_name,
            "email": db_provider.email,
            "phone": db_provider.phone,
            "status": db_provider.status
        }
        
        # Add history entry
        history_entry = ServiceProviderHistory(
            provider_id=provider_id,
            action="updated",
            description=f"Prestador de serviço atualizado: {', '.join(update_dict.keys())}",
            changed_by="Sistema",
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def activate_service_provider(self, provider_id: int, activated_by: str) -> Optional[ServiceProvider]:
        db_provider = self.get_service_provider(provider_id)
        if not db_provider:
            return None
        
        # Store old values for history
        old_values = {"status": db_provider.status}
        
        db_provider.status = "active"
        db_provider.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_provider.status}
        
        # Add history entry
        history_entry = ServiceProviderHistory(
            provider_id=provider_id,
            action="activated",
            description="Prestador de serviço ativado",
            changed_by=activated_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def deactivate_service_provider(self, provider_id: int, deactivated_by: str) -> Optional[ServiceProvider]:
        db_provider = self.get_service_provider(provider_id)
        if not db_provider:
            return None
        
        # Store old values for history
        old_values = {"status": db_provider.status}
        
        db_provider.status = "inactive"
        db_provider.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_provider.status}
        
        # Add history entry
        history_entry = ServiceProviderHistory(
            provider_id=provider_id,
            action="deactivated",
            description="Prestador de serviço desativado",
            changed_by=deactivated_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def suspend_service_provider(self, provider_id: int, suspended_by: str) -> Optional[ServiceProvider]:
        db_provider = self.get_service_provider(provider_id)
        if not db_provider:
            return None
        
        # Store old values for history
        old_values = {"status": db_provider.status}
        
        db_provider.status = "suspended"
        db_provider.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_provider.status}
        
        # Add history entry
        history_entry = ServiceProviderHistory(
            provider_id=provider_id,
            action="suspended",
            description="Prestador de serviço suspenso",
            changed_by=suspended_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def reject_service_provider(self, provider_id: int, rejected_by: str) -> Optional[ServiceProvider]:
        db_provider = self.get_service_provider(provider_id)
        if not db_provider:
            return None
        
        # Store old values for history
        old_values = {"status": db_provider.status}
        
        db_provider.status = "rejected"
        db_provider.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_provider.status}
        
        # Add history entry
        history_entry = ServiceProviderHistory(
            provider_id=provider_id,
            action="rejected",
            description="Prestador de serviço rejeitado",
            changed_by=rejected_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def delete_service_provider(self, provider_id: int) -> bool:
        db_provider = self.get_service_provider(provider_id)
        if not db_provider:
            return False
        
        self.db.delete(db_provider)
        self.db.commit()
        return True

    def get_service_provider_history(self, provider_id: int) -> List[ServiceProviderHistory]:
        return self.db.query(ServiceProviderHistory).filter(
            ServiceProviderHistory.provider_id == provider_id
        ).order_by(desc(ServiceProviderHistory.created_at)).all()

    def add_service_provider_history(self, history_data: ServiceProviderHistoryIn) -> ServiceProviderHistory:
        db_history = ServiceProviderHistory(
            provider_id=history_data.provider_id,
            action=history_data.action,
            description=history_data.description,
            changed_by=history_data.changed_by,
            old_values=history_data.old_values,
            new_values=history_data.new_values
        )
        
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def add_service_provider_rating(self, rating_data: ServiceProviderRatingIn) -> ServiceProviderRating:
        db_rating = ServiceProviderRating(
            provider_id=rating_data.provider_id,
            rating=rating_data.rating,
            comment=rating_data.comment,
            rated_by=rating_data.rated_by,
            service_date=rating_data.service_date
        )
        
        self.db.add(db_rating)
        self.db.commit()
        self.db.refresh(db_rating)
        
        # Update provider's average rating
        self.update_provider_rating(rating_data.provider_id)
        
        return db_rating

    def update_provider_rating(self, provider_id: int) -> Optional[ServiceProvider]:
        db_provider = self.get_service_provider(provider_id)
        if not db_provider:
            return None
        
        # Calculate average rating
        ratings = self.db.query(ServiceProviderRating).filter(
            ServiceProviderRating.provider_id == provider_id
        ).all()
        
        if ratings:
            total_rating = sum(rating.rating for rating in ratings)
            average_rating = total_rating / len(ratings)
            db_provider.rating = round(average_rating, 2)
        else:
            db_provider.rating = 0.0
        
        self.db.commit()
        self.db.refresh(db_provider)
        return db_provider

    def get_service_provider_ratings(self, provider_id: int) -> List[ServiceProviderRating]:
        return self.db.query(ServiceProviderRating).filter(
            ServiceProviderRating.provider_id == provider_id
        ).order_by(desc(ServiceProviderRating.created_at)).all()

    def get_service_providers_by_service_type(self, service_type: str) -> List[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(
            ServiceProvider.service_types.contains([service_type])
        ).order_by(desc(ServiceProvider.rating)).all()

    def get_service_providers_by_city(self, city: str) -> List[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(
            ServiceProvider.city.ilike(f"%{city}%")
        ).order_by(desc(ServiceProvider.rating)).all()

    def get_service_providers_by_state(self, state: str) -> List[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(
            ServiceProvider.state == state
        ).order_by(desc(ServiceProvider.rating)).all()

    def get_contractors(self) -> List[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(
            ServiceProvider.is_contractor == True
        ).order_by(desc(ServiceProvider.created_at)).all()

    def get_top_rated_providers(self, limit: int = 10) -> List[ServiceProvider]:
        return self.db.query(ServiceProvider).filter(
            ServiceProvider.rating > 0
        ).order_by(desc(ServiceProvider.rating)).limit(limit).all()

    def get_recent_providers(self, limit: int = 10) -> List[ServiceProvider]:
        return self.db.query(ServiceProvider).order_by(
            desc(ServiceProvider.created_at)
        ).limit(limit).all()

    def get_service_provider_stats(self) -> Dict[str, Any]:
        total_providers = self.db.query(ServiceProvider).count()
        
        status_counts = {}
        for status in ["active", "inactive", "suspended", "pending", "rejected"]:
            status_counts[status] = self.db.query(ServiceProvider).filter(
                ServiceProvider.status == status
            ).count()
        
        contractors = self.db.query(ServiceProvider).filter(
            ServiceProvider.is_contractor == True
        ).count()
        
        non_contractors = total_providers - contractors
        
        # Service type breakdown
        service_type_breakdown = {}
        providers = self.db.query(ServiceProvider).all()
        for provider in providers:
            for service_type in provider.service_types:
                service_type_breakdown[service_type] = service_type_breakdown.get(service_type, 0) + 1
        
        # City breakdown
        city_breakdown = {}
        city_counts = self.db.query(
            ServiceProvider.city, 
            func.count(ServiceProvider.id)
        ).group_by(ServiceProvider.city).all()
        
        for city, count in city_counts:
            city_breakdown[city] = count
        
        # State breakdown
        state_breakdown = {}
        state_counts = self.db.query(
            ServiceProvider.state, 
            func.count(ServiceProvider.id)
        ).group_by(ServiceProvider.state).all()
        
        for state, count in state_counts:
            state_breakdown[state] = count
        
        # Average rating
        avg_rating = self.db.query(func.avg(ServiceProvider.rating)).scalar()
        average_rating = round(avg_rating, 2) if avg_rating else 0.0
        
        # Top rated providers
        top_rated = self.get_top_rated_providers(5)
        top_rated_data = [
            {
                "id": provider.id,
                "name": provider.name,
                "company_name": provider.company_name,
                "rating": provider.rating
            }
            for provider in top_rated
        ]
        
        # Recent providers
        recent_providers = self.get_recent_providers(5)
        recent_data = [
            {
                "id": provider.id,
                "name": provider.name,
                "company_name": provider.company_name,
                "created_at": provider.created_at
            }
            for provider in recent_providers
        ]
        
        return {
            "total_providers": total_providers,
            "active_providers": status_counts["active"],
            "inactive_providers": status_counts["inactive"],
            "suspended_providers": status_counts["suspended"],
            "pending_providers": status_counts["pending"],
            "rejected_providers": status_counts["rejected"],
            "contractors": contractors,
            "non_contractors": non_contractors,
            "service_type_breakdown": service_type_breakdown,
            "city_breakdown": city_breakdown,
            "state_breakdown": state_breakdown,
            "average_rating": average_rating,
            "top_rated_providers": top_rated_data,
            "recent_providers": recent_data
        }

