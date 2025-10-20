from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.assets import AssetIn, AssetOut, AssetUpdate, AssetHistoryIn, AssetMaintenanceIn, AssetDisposalIn
from ..services.asset_service import AssetService
from datetime import datetime, date

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/", response_model=AssetOut)
def create_asset(asset_data: AssetIn, created_by: str = "Sistema", db: Session = Depends(get_db)):
    service = AssetService(db)
    try:
        return service.create_asset(asset_data, created_by)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[AssetOut])
def list_assets(
    asset_type: Optional[str] = None,
    status: Optional[str] = None,
    condition: Optional[str] = None,
    location: Optional[str] = None,
    unit_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    return service.list_assets(asset_type, status, condition, location, unit_id)


@router.get("/search/{search_term}")
def search_assets(search_term: str, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.search_assets(search_term)


@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    service = AssetService(db)
    asset = service.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return asset


@router.get("/serial/{serial_number}", response_model=AssetOut)
def get_asset_by_serial(serial_number: str, db: Session = Depends(get_db)):
    service = AssetService(db)
    asset = service.get_asset_by_serial(serial_number)
    if not asset:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return asset


@router.put("/{asset_id}", response_model=AssetOut)
def update_asset(
    asset_id: int,
    update_data: AssetUpdate,
    changed_by: str = "Sistema",
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    asset = service.update_asset(asset_id, update_data, changed_by)
    if not asset:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return asset


@router.post("/{asset_id}/dispose", response_model=AssetOut)
def dispose_asset(
    asset_id: int,
    disposal_data: AssetDisposalIn,
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    asset = service.dispose_asset(asset_id, disposal_data)
    if not asset:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return asset


@router.post("/{asset_id}/lost")
def mark_asset_lost(
    asset_id: int,
    lost_by: str,
    reason: str,
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    asset = service.mark_asset_lost(asset_id, lost_by, reason)
    if not asset:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return {"message": "Patrimônio marcado como perdido"}


@router.post("/{asset_id}/stolen")
def mark_asset_stolen(
    asset_id: int,
    stolen_by: str,
    reason: str,
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    asset = service.mark_asset_stolen(asset_id, stolen_by, reason)
    if not asset:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return {"message": "Patrimônio marcado como roubado"}


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    service = AssetService(db)
    success = service.delete_asset(asset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return {"message": "Patrimônio excluído com sucesso"}


@router.get("/{asset_id}/history")
def get_asset_history(asset_id: int, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_asset_history(asset_id)


@router.get("/{asset_id}/value-history")
def get_asset_value_history(asset_id: int, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_asset_value_history(asset_id)


@router.get("/{asset_id}/location-history")
def get_asset_location_history(asset_id: int, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_asset_location_history(asset_id)


@router.get("/{asset_id}/condition-history")
def get_asset_condition_history(asset_id: int, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_asset_condition_history(asset_id)


@router.post("/{asset_id}/history", response_model=dict)
def add_asset_history(
    asset_id: int,
    history_data: AssetHistoryIn,
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    history_data.asset_id = asset_id
    return service.add_asset_history(history_data)


@router.post("/{asset_id}/maintenance", response_model=dict)
def create_maintenance_record(
    asset_id: int,
    maintenance_data: AssetMaintenanceIn,
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    maintenance_data.asset_id = asset_id
    return service.create_maintenance_record(maintenance_data)


@router.get("/{asset_id}/maintenance")
def get_asset_maintenance(asset_id: int, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_asset_maintenance(asset_id)


@router.get("/type/{asset_type}")
def get_assets_by_type(asset_type: str, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_by_type(asset_type)


@router.get("/status/{status}")
def get_assets_by_status(status: str, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_by_status(status)


@router.get("/condition/{condition}")
def get_assets_by_condition(condition: str, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_by_condition(condition)


@router.get("/location/{location}")
def get_assets_by_location(location: str, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_by_location(location)


@router.get("/responsible/{responsible_person}")
def get_assets_by_responsible_person(responsible_person: str, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_by_responsible_person(responsible_person)


@router.get("/unit/{unit_id}")
def get_assets_by_unit(unit_id: int, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_by_unit(unit_id)


@router.get("/maintenance/required")
def get_assets_requiring_maintenance(db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_requiring_maintenance()


@router.get("/warranty/expired")
def get_assets_with_expired_warranty(db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_with_expired_warranty()


@router.get("/creator/{created_by}")
def get_assets_by_creator(created_by: str, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.get_assets_by_creator(created_by)


@router.get("/date-range")
def get_assets_by_date_range(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AssetService(db)
    return service.get_assets_by_date_range(start, end)


@router.get("/value-range")
def get_assets_by_value_range(
    min_value: float,
    max_value: float,
    db: Session = Depends(get_db)
):
    service = AssetService(db)
    return service.get_assets_by_value_range(min_value, max_value)


@router.get("/stats/summary")
def get_assets_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AssetService(db)
    return service.get_assets_stats(start, end)


