from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.asset_repository import AssetRepository
from ..schemas.assets import AssetIn, AssetOut, AssetUpdate, AssetHistoryIn, AssetMaintenanceIn, AssetDisposalIn
from datetime import datetime, date


class AssetService:
    def __init__(self, db: Session):
        self.repository = AssetRepository(db)

    def create_asset(self, asset_data: AssetIn, created_by: str = "Sistema") -> AssetOut:
        # Check if asset with same serial number already exists
        if asset_data.serial_number:
            existing_asset = self.repository.get_asset_by_serial(asset_data.serial_number)
            if existing_asset:
                raise ValueError("Já existe um patrimônio com este número de série")
        
        asset = self.repository.create_asset(asset_data)
        return AssetOut.from_orm(asset)

    def get_asset(self, asset_id: int) -> Optional[AssetOut]:
        asset = self.repository.get_asset(asset_id)
        if asset:
            return AssetOut.from_orm(asset)
        return None

    def get_asset_by_serial(self, serial_number: str) -> Optional[AssetOut]:
        asset = self.repository.get_asset_by_serial(serial_number)
        if asset:
            return AssetOut.from_orm(asset)
        return None

    def list_assets(self, 
                   asset_type: Optional[str] = None,
                   status: Optional[str] = None,
                   condition: Optional[str] = None,
                   location: Optional[str] = None,
                   unit_id: Optional[int] = None) -> List[AssetOut]:
        assets = self.repository.list_assets(asset_type, status, condition, location, unit_id)
        return [AssetOut.from_orm(asset) for asset in assets]

    def search_assets(self, search_term: str) -> List[AssetOut]:
        assets = self.repository.search_assets(search_term)
        return [AssetOut.from_orm(asset) for asset in assets]

    def update_asset(self, asset_id: int, update_data: AssetUpdate, changed_by: str = "Sistema") -> Optional[AssetOut]:
        asset = self.repository.update_asset(asset_id, update_data)
        if asset:
            return AssetOut.from_orm(asset)
        return None

    def dispose_asset(self, asset_id: int, disposal_data: AssetDisposalIn) -> Optional[AssetOut]:
        asset = self.repository.dispose_asset(asset_id, disposal_data)
        if asset:
            return AssetOut.from_orm(asset)
        return None

    def mark_asset_lost(self, asset_id: int, lost_by: str, reason: str) -> Optional[AssetOut]:
        asset = self.repository.mark_asset_lost(asset_id, lost_by, reason)
        if asset:
            return AssetOut.from_orm(asset)
        return None

    def mark_asset_stolen(self, asset_id: int, stolen_by: str, reason: str) -> Optional[AssetOut]:
        asset = self.repository.mark_asset_stolen(asset_id, stolen_by, reason)
        if asset:
            return AssetOut.from_orm(asset)
        return None

    def delete_asset(self, asset_id: int) -> bool:
        return self.repository.delete_asset(asset_id)

    def get_asset_history(self, asset_id: int) -> List[dict]:
        history = self.repository.get_asset_history(asset_id)
        return [
            {
                "id": entry.id,
                "action": entry.action,
                "description": entry.description,
                "changed_by": entry.changed_by,
                "old_values": entry.old_values,
                "new_values": entry.new_values,
                "created_at": entry.created_at
            }
            for entry in history
        ]

    def add_asset_history(self, history_data: AssetHistoryIn) -> dict:
        history = self.repository.add_asset_history(history_data)
        return {
            "id": history.id,
            "asset_id": history.asset_id,
            "action": history.action,
            "description": history.description,
            "changed_by": history.changed_by,
            "old_values": history.old_values,
            "new_values": history.new_values,
            "created_at": history.created_at
        }

    def create_maintenance_record(self, maintenance_data: AssetMaintenanceIn) -> dict:
        maintenance = self.repository.create_maintenance_record(maintenance_data)
        return {
            "id": maintenance.id,
            "asset_id": maintenance.asset_id,
            "maintenance_type": maintenance.maintenance_type,
            "description": maintenance.description,
            "cost": maintenance.cost,
            "performed_by": maintenance.performed_by,
            "maintenance_date": maintenance.maintenance_date,
            "next_maintenance_date": maintenance.next_maintenance_date,
            "notes": maintenance.notes,
            "created_at": maintenance.created_at
        }

    def get_asset_maintenance(self, asset_id: int) -> List[dict]:
        maintenance = self.repository.get_asset_maintenance(asset_id)
        return [
            {
                "id": entry.id,
                "asset_id": entry.asset_id,
                "maintenance_type": entry.maintenance_type,
                "description": entry.description,
                "cost": entry.cost,
                "performed_by": entry.performed_by,
                "maintenance_date": entry.maintenance_date,
                "next_maintenance_date": entry.next_maintenance_date,
                "notes": entry.notes,
                "created_at": entry.created_at
            }
            for entry in maintenance
        ]

    def get_assets_by_type(self, asset_type: str) -> List[AssetOut]:
        assets = self.repository.get_assets_by_type(asset_type)
        return [AssetOut.from_orm(asset) for asset in assets]

    def get_assets_by_status(self, status: str) -> List[AssetOut]:
        assets = self.repository.get_assets_by_status(status)
        return [AssetOut.from_orm(asset) for asset in assets]

    def get_assets_by_condition(self, condition: str) -> List[AssetOut]:
        assets = self.repository.get_assets_by_condition(condition)
        return [AssetOut.from_orm(asset) for asset in assets]

    def get_assets_by_location(self, location: str) -> List[AssetOut]:
        assets = self.repository.get_assets_by_location(location)
        return [AssetOut.from_orm(asset) for asset in assets]

    def get_assets_by_responsible_person(self, responsible_person: str) -> List[AssetOut]:
        assets = self.repository.get_assets_by_responsible_person(responsible_person)
        return [AssetOut.from_orm(asset) for asset in assets]

    def get_assets_requiring_maintenance(self) -> List[AssetOut]:
        assets = self.repository.get_assets_requiring_maintenance()
        return [AssetOut.from_orm(asset) for asset in assets]

    def get_assets_with_expired_warranty(self) -> List[AssetOut]:
        assets = self.repository.get_assets_with_expired_warranty()
        return [AssetOut.from_orm(asset) for asset in assets]

    def get_assets_stats(self, start_date: date, end_date: date) -> dict:
        return self.repository.get_assets_stats(start_date, end_date)

    def get_assets_by_unit(self, unit_id: int) -> List[AssetOut]:
        assets = self.repository.list_assets(unit_id=unit_id)
        return [AssetOut.from_orm(asset) for asset in assets]

    def get_assets_by_creator(self, created_by: str) -> List[AssetOut]:
        # This would need to be implemented in the repository
        # For now, we'll use a simple approach
        assets = self.repository.list_assets()
        filtered_assets = []
        
        for asset in assets:
            if created_by.lower() in asset.created_by.lower():
                filtered_assets.append(asset)
        
        return [AssetOut.from_orm(asset) for asset in filtered_assets]

    def get_asset_value_history(self, asset_id: int) -> List[dict]:
        """Get value change history for an asset"""
        history = self.repository.get_asset_history(asset_id)
        value_history = []
        
        for entry in history:
            if entry.action in ["created", "updated"] and entry.new_values and "purchase_price" in entry.new_values:
                value_history.append({
                    "id": entry.id,
                    "action": entry.action,
                    "old_value": entry.old_values.get("purchase_price") if entry.old_values else None,
                    "new_value": entry.new_values.get("purchase_price"),
                    "changed_by": entry.changed_by,
                    "created_at": entry.created_at
                })
        
        return value_history

    def get_asset_location_history(self, asset_id: int) -> List[dict]:
        """Get location change history for an asset"""
        history = self.repository.get_asset_history(asset_id)
        location_history = []
        
        for entry in history:
            if entry.action in ["created", "updated"] and entry.new_values and "location" in entry.new_values:
                location_history.append({
                    "id": entry.id,
                    "action": entry.action,
                    "old_location": entry.old_values.get("location") if entry.old_values else None,
                    "new_location": entry.new_values.get("location"),
                    "changed_by": entry.changed_by,
                    "created_at": entry.created_at
                })
        
        return location_history

    def get_asset_condition_history(self, asset_id: int) -> List[dict]:
        """Get condition change history for an asset"""
        history = self.repository.get_asset_history(asset_id)
        condition_history = []
        
        for entry in history:
            if entry.action in ["created", "updated"] and entry.new_values and "condition" in entry.new_values:
                condition_history.append({
                    "id": entry.id,
                    "action": entry.action,
                    "old_condition": entry.old_values.get("condition") if entry.old_values else None,
                    "new_condition": entry.new_values.get("condition"),
                    "changed_by": entry.changed_by,
                    "created_at": entry.created_at
                })
        
        return condition_history

    def get_assets_by_date_range(self, start_date: date, end_date: date) -> List[AssetOut]:
        assets = self.repository.list_assets()
        filtered_assets = []
        
        for asset in assets:
            if start_date <= asset.purchase_date <= end_date:
                filtered_assets.append(asset)
        
        return [AssetOut.from_orm(asset) for asset in filtered_assets]

    def get_assets_by_value_range(self, min_value: float, max_value: float) -> List[AssetOut]:
        assets = self.repository.list_assets()
        filtered_assets = []
        
        for asset in assets:
            if min_value <= asset.purchase_price <= max_value:
                filtered_assets.append(asset)
        
        return [AssetOut.from_orm(asset) for asset in filtered_assets]


