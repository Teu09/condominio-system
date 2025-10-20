from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.assets import Asset, AssetHistory, AssetMaintenance
from ..schemas.assets import AssetIn, AssetUpdate, AssetHistoryIn, AssetMaintenanceIn, AssetDisposalIn
from datetime import datetime, date


class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_asset(self, asset_data: AssetIn) -> Asset:
        db_asset = Asset(
            name=asset_data.name,
            description=asset_data.description,
            asset_type=asset_data.asset_type,
            brand=asset_data.brand,
            model=asset_data.model,
            serial_number=asset_data.serial_number,
            purchase_date=asset_data.purchase_date,
            purchase_price=asset_data.purchase_price,
            supplier=asset_data.supplier,
            warranty_expires=asset_data.warranty_expires,
            location=asset_data.location,
            condition=asset_data.condition,
            status=asset_data.status,
            responsible_person=asset_data.responsible_person,
            maintenance_schedule=asset_data.maintenance_schedule,
            notes=asset_data.notes,
            unit_id=asset_data.unit_id,
            created_by="Sistema"  # This should be passed from the service
        )
        
        self.db.add(db_asset)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = AssetHistory(
            asset_id=db_asset.id,
            action="created",
            description="Patrimônio cadastrado",
            changed_by="Sistema"
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def get_asset(self, asset_id: int) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def get_asset_by_serial(self, serial_number: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.serial_number == serial_number).first()

    def list_assets(self, 
                   asset_type: Optional[str] = None,
                   status: Optional[str] = None,
                   condition: Optional[str] = None,
                   location: Optional[str] = None,
                   unit_id: Optional[int] = None) -> List[Asset]:
        query = self.db.query(Asset)
        
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)
        if status:
            query = query.filter(Asset.status == status)
        if condition:
            query = query.filter(Asset.condition == condition)
        if location:
            query = query.filter(Asset.location.ilike(f"%{location}%"))
        if unit_id:
            query = query.filter(Asset.unit_id == unit_id)
            
        return query.order_by(Asset.name.asc()).all()

    def search_assets(self, search_term: str) -> List[Asset]:
        return self.db.query(Asset).filter(
            (Asset.name.ilike(f"%{search_term}%")) |
            (Asset.description.ilike(f"%{search_term}%")) |
            (Asset.brand.ilike(f"%{search_term}%")) |
            (Asset.model.ilike(f"%{search_term}%")) |
            (Asset.serial_number.ilike(f"%{search_term}%"))
        ).order_by(Asset.name.asc()).all()

    def update_asset(self, asset_id: int, update_data: AssetUpdate) -> Optional[Asset]:
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return None
        
        # Store old values for history
        old_values = {
            "name": db_asset.name,
            "location": db_asset.location,
            "condition": db_asset.condition,
            "status": db_asset.status,
            "responsible_person": db_asset.responsible_person
        }
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_asset, field, value)
        
        db_asset.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "name": db_asset.name,
            "location": db_asset.location,
            "condition": db_asset.condition,
            "status": db_asset.status,
            "responsible_person": db_asset.responsible_person
        }
        
        # Add history entry
        history_entry = AssetHistory(
            asset_id=asset_id,
            action="updated",
            description=f"Patrimônio atualizado: {', '.join(update_dict.keys())}",
            changed_by="Sistema",
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def dispose_asset(self, asset_id: int, disposal_data: AssetDisposalIn) -> Optional[Asset]:
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return None
        
        # Store old values for history
        old_values = {
            "status": db_asset.status,
            "disposal_date": db_asset.disposal_date,
            "disposal_reason": db_asset.disposal_reason
        }
        
        db_asset.status = "disposed"
        db_asset.disposal_date = disposal_data.disposal_date
        db_asset.disposal_reason = disposal_data.disposal_reason
        db_asset.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "status": db_asset.status,
            "disposal_date": db_asset.disposal_date,
            "disposal_reason": db_asset.disposal_reason
        }
        
        # Add history entry
        history_entry = AssetHistory(
            asset_id=asset_id,
            action="disposed",
            description=f"Patrimônio descartado: {disposal_data.disposal_reason}",
            changed_by=disposal_data.disposed_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def mark_asset_lost(self, asset_id: int, lost_by: str, reason: str) -> Optional[Asset]:
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return None
        
        # Store old values for history
        old_values = {"status": db_asset.status}
        
        db_asset.status = "lost"
        db_asset.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_asset.status}
        
        # Add history entry
        history_entry = AssetHistory(
            asset_id=asset_id,
            action="lost",
            description=f"Patrimônio perdido: {reason}",
            changed_by=lost_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def mark_asset_stolen(self, asset_id: int, stolen_by: str, reason: str) -> Optional[Asset]:
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return None
        
        # Store old values for history
        old_values = {"status": db_asset.status}
        
        db_asset.status = "stolen"
        db_asset.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_asset.status}
        
        # Add history entry
        history_entry = AssetHistory(
            asset_id=asset_id,
            action="stolen",
            description=f"Patrimônio roubado: {reason}",
            changed_by=stolen_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def delete_asset(self, asset_id: int) -> bool:
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return False
        
        self.db.delete(db_asset)
        self.db.commit()
        return True

    def get_asset_history(self, asset_id: int) -> List[AssetHistory]:
        return self.db.query(AssetHistory).filter(
            AssetHistory.asset_id == asset_id
        ).order_by(AssetHistory.created_at.desc()).all()

    def add_asset_history(self, history_data: AssetHistoryIn) -> AssetHistory:
        db_history = AssetHistory(
            asset_id=history_data.asset_id,
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

    def create_maintenance_record(self, maintenance_data: AssetMaintenanceIn) -> AssetMaintenance:
        db_maintenance = AssetMaintenance(
            asset_id=maintenance_data.asset_id,
            maintenance_type=maintenance_data.maintenance_type,
            description=maintenance_data.description,
            cost=maintenance_data.cost,
            performed_by=maintenance_data.performed_by,
            maintenance_date=maintenance_data.maintenance_date,
            next_maintenance_date=maintenance_data.next_maintenance_date,
            notes=maintenance_data.notes
        )
        
        self.db.add(db_maintenance)
        self.db.flush()  # Get the ID
        
        # Add history entry
        history_entry = AssetHistory(
            asset_id=maintenance_data.asset_id,
            action="maintenance",
            description=f"Manutenção realizada: {maintenance_data.maintenance_type}",
            changed_by=maintenance_data.performed_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_maintenance)
        return db_maintenance

    def get_asset_maintenance(self, asset_id: int) -> List[AssetMaintenance]:
        return self.db.query(AssetMaintenance).filter(
            AssetMaintenance.asset_id == asset_id
        ).order_by(AssetMaintenance.maintenance_date.desc()).all()

    def get_assets_by_type(self, asset_type: str) -> List[Asset]:
        return self.db.query(Asset).filter(
            Asset.asset_type == asset_type
        ).order_by(Asset.name.asc()).all()

    def get_assets_by_status(self, status: str) -> List[Asset]:
        return self.db.query(Asset).filter(
            Asset.status == status
        ).order_by(Asset.name.asc()).all()

    def get_assets_by_condition(self, condition: str) -> List[Asset]:
        return self.db.query(Asset).filter(
            Asset.condition == condition
        ).order_by(Asset.name.asc()).all()

    def get_assets_by_location(self, location: str) -> List[Asset]:
        return self.db.query(Asset).filter(
            Asset.location.ilike(f"%{location}%")
        ).order_by(Asset.name.asc()).all()

    def get_assets_by_responsible_person(self, responsible_person: str) -> List[Asset]:
        return self.db.query(Asset).filter(
            Asset.responsible_person == responsible_person
        ).order_by(Asset.name.asc()).all()

    def get_assets_requiring_maintenance(self) -> List[Asset]:
        today = date.today()
        return self.db.query(Asset).filter(
            Asset.status == "active",
            Asset.maintenance_schedule.isnot(None)
        ).all()

    def get_assets_with_expired_warranty(self) -> List[Asset]:
        today = date.today()
        return self.db.query(Asset).filter(
            Asset.warranty_expires < today,
            Asset.status == "active"
        ).order_by(Asset.warranty_expires.asc()).all()

    def get_assets_stats(self, start_date: date, end_date: date) -> dict:
        query = self.db.query(Asset).filter(
            Asset.purchase_date >= start_date,
            Asset.purchase_date <= end_date
        )
        
        total_assets = query.count()
        total_value = sum([asset.purchase_price for asset in query.all()])
        
        type_breakdown = {}
        status_breakdown = {}
        condition_breakdown = {}
        
        for asset in query.all():
            type_breakdown[asset.asset_type] = type_breakdown.get(asset.asset_type, 0) + 1
            status_breakdown[asset.status] = status_breakdown.get(asset.status, 0) + 1
            condition_breakdown[asset.condition] = condition_breakdown.get(asset.condition, 0) + 1
        
        return {
            "total_assets": total_assets,
            "total_value": total_value,
            "type_breakdown": type_breakdown,
            "status_breakdown": status_breakdown,
            "condition_breakdown": condition_breakdown
        }


