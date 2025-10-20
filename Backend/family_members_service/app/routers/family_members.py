from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.family_members import (
    FamilyMemberIn, FamilyMemberOut, FamilyMemberUpdate, 
    FamilyMemberHistoryIn, FamilyMemberHistoryOut, 
    FamilyMemberSearchIn, FamilyMemberStatsOut, FamilyTreeOut,
    FamilyMemberDocumentIn, FamilyMemberDocumentOut
)
from ..services.family_member_service import FamilyMemberService
from datetime import date

router = APIRouter(prefix="/family-members", tags=["family-members"])


@router.post("/", response_model=FamilyMemberOut)
def create_family_member(member_data: FamilyMemberIn, created_by: str = "Sistema", db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.create_family_member(member_data, created_by)


@router.get("/", response_model=List[FamilyMemberOut])
def list_family_members(
    unit_id: Optional[int] = None,
    main_resident_id: Optional[int] = None,
    relationship_type: Optional[str] = None,
    gender: Optional[str] = None,
    marital_status: Optional[str] = None,
    is_emergency_contact: Optional[bool] = None,
    is_authorized_visitor: Optional[bool] = None,
    is_resident: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    service = FamilyMemberService(db)
    return service.list_family_members(
        unit_id, main_resident_id, relationship_type, gender, marital_status,
        is_emergency_contact, is_authorized_visitor, is_resident
    )


@router.post("/search", response_model=List[FamilyMemberOut])
def search_family_members(search_data: FamilyMemberSearchIn, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.search_family_members(search_data)


@router.get("/{member_id}", response_model=FamilyMemberOut)
def get_family_member(member_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    member = service.get_family_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Membro da família não encontrado")
    return member


@router.get("/cpf/{cpf}", response_model=FamilyMemberOut)
def get_family_member_by_cpf(cpf: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    member = service.get_family_member_by_cpf(cpf)
    if not member:
        raise HTTPException(status_code=404, detail="Membro da família não encontrado")
    return member


@router.get("/rg/{rg}", response_model=FamilyMemberOut)
def get_family_member_by_rg(rg: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    member = service.get_family_member_by_rg(rg)
    if not member:
        raise HTTPException(status_code=404, detail="Membro da família não encontrado")
    return member


@router.get("/email/{email}", response_model=FamilyMemberOut)
def get_family_member_by_email(email: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    member = service.get_family_member_by_email(email)
    if not member:
        raise HTTPException(status_code=404, detail="Membro da família não encontrado")
    return member


@router.put("/{member_id}", response_model=FamilyMemberOut)
def update_family_member(
    member_id: int,
    update_data: FamilyMemberUpdate,
    changed_by: str = "Sistema",
    db: Session = Depends(get_db)
):
    service = FamilyMemberService(db)
    member = service.update_family_member(member_id, update_data, changed_by)
    if not member:
        raise HTTPException(status_code=404, detail="Membro da família não encontrado")
    return member


@router.delete("/{member_id}")
def delete_family_member(member_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    success = service.delete_family_member(member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Membro da família não encontrado")
    return {"message": "Membro da família excluído com sucesso"}


@router.get("/{member_id}/history")
def get_family_member_history(member_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_member_history(member_id)


@router.post("/{member_id}/history", response_model=FamilyMemberHistoryOut)
def add_family_member_history(
    member_id: int,
    history_data: FamilyMemberHistoryIn,
    db: Session = Depends(get_db)
):
    service = FamilyMemberService(db)
    history_data.member_id = member_id
    return service.add_family_member_history(history_data)


@router.get("/unit/{unit_id}")
def get_family_members_by_unit(unit_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_unit(unit_id)


@router.get("/main-resident/{main_resident_id}")
def get_family_members_by_main_resident(main_resident_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_main_resident(main_resident_id)


@router.get("/relationship/{relationship_type}")
def get_family_members_by_relationship(relationship_type: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_relationship(relationship_type)


@router.get("/emergency-contacts/list")
def get_emergency_contacts(unit_id: Optional[int] = None, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_emergency_contacts(unit_id)


@router.get("/authorized-visitors/list")
def get_authorized_visitors(unit_id: Optional[int] = None, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_authorized_visitors(unit_id)


@router.get("/residents/list")
def get_residents(unit_id: Optional[int] = None, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_residents(unit_id)


@router.get("/age-range/list")
def get_family_members_by_age_range(
    min_age: int = Query(0, ge=0, le=120),
    max_age: int = Query(120, ge=0, le=120),
    db: Session = Depends(get_db)
):
    service = FamilyMemberService(db)
    return service.get_family_members_by_age_range(min_age, max_age)


@router.get("/gender/{gender}")
def get_family_members_by_gender(gender: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_gender(gender)


@router.get("/marital-status/{marital_status}")
def get_family_members_by_marital_status(marital_status: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_marital_status(marital_status)


@router.get("/city/{city}")
def get_family_members_by_city(city: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_city(city)


@router.get("/state/{state}")
def get_family_members_by_state(state: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_state(state)


@router.get("/occupation/{occupation}")
def get_family_members_by_occupation(occupation: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_occupation(occupation)


@router.get("/recent/list")
def get_recent_family_members(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_recent_family_members(limit)


@router.get("/stats/summary")
def get_family_member_stats(db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_member_stats()


@router.get("/family-tree/{main_resident_id}")
def get_family_tree(main_resident_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_tree(main_resident_id)


@router.get("/search/name/{name}")
def get_family_members_by_name(name: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_name(name)


@router.get("/search/cpf/{cpf}")
def get_family_members_by_cpf(cpf: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_cpf(cpf)


@router.get("/search/rg/{rg}")
def get_family_members_by_rg(rg: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_rg(rg)


@router.get("/search/email/{email}")
def get_family_members_by_email(email: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_email(email)


@router.get("/search/relationship/{relationship_type}")
def get_family_members_by_relationship_type(relationship_type: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_relationship_type(relationship_type)


@router.get("/search/gender/{gender}")
def get_family_members_by_gender_type(gender: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_gender_type(gender)


@router.get("/search/marital-status/{marital_status}")
def get_family_members_by_marital_status_type(marital_status: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_marital_status_type(marital_status)


@router.get("/search/emergency-contact/{is_emergency_contact}")
def get_family_members_by_emergency_contact_status(is_emergency_contact: bool, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_emergency_contact_status(is_emergency_contact)


@router.get("/search/authorized-visitor/{is_authorized_visitor}")
def get_family_members_by_authorized_visitor_status(is_authorized_visitor: bool, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_authorized_visitor_status(is_authorized_visitor)


@router.get("/search/resident/{is_resident}")
def get_family_members_by_resident_status(is_resident: bool, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_resident_status(is_resident)


@router.get("/search/location/{city}/{state}")
def get_family_members_by_location(city: str, state: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_location(city, state)


@router.get("/search/occupation/{occupation}")
def get_family_members_by_occupation_type(occupation: str, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_members_by_occupation_type(occupation)


# Document endpoints
@router.post("/{member_id}/documents", response_model=FamilyMemberDocumentOut)
def create_family_member_document(
    member_id: int,
    document_data: FamilyMemberDocumentIn,
    db: Session = Depends(get_db)
):
    service = FamilyMemberService(db)
    document_data.member_id = member_id
    return service.create_family_member_document(document_data)


@router.get("/{member_id}/documents")
def get_family_member_documents(member_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    return service.get_family_member_documents(member_id)


@router.get("/documents/{document_id}", response_model=FamilyMemberDocumentOut)
def get_family_member_document(document_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    document = service.get_family_member_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document


@router.put("/documents/{document_id}", response_model=FamilyMemberDocumentOut)
def update_family_member_document(
    document_id: int,
    update_data: dict,
    db: Session = Depends(get_db)
):
    service = FamilyMemberService(db)
    document = service.update_family_member_document(document_id, update_data)
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document


@router.delete("/documents/{document_id}")
def delete_family_member_document(document_id: int, db: Session = Depends(get_db)):
    service = FamilyMemberService(db)
    success = service.delete_family_member_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return {"message": "Documento excluído com sucesso"}

