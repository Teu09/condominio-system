from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..repositories.family_member_repository import FamilyMemberRepository
from ..schemas.family_members import (
    FamilyMemberIn, FamilyMemberOut, FamilyMemberUpdate, 
    FamilyMemberHistoryIn, FamilyMemberHistoryOut, 
    FamilyMemberSearchIn, FamilyMemberStatsOut, FamilyTreeOut,
    FamilyMemberDocumentIn, FamilyMemberDocumentOut
)
from datetime import datetime, date


class FamilyMemberService:
    def __init__(self, db: Session):
        self.repository = FamilyMemberRepository(db)

    def create_family_member(self, member_data: FamilyMemberIn, created_by: str = "Sistema") -> FamilyMemberOut:
        member = self.repository.create_family_member(member_data)
        return FamilyMemberOut.from_orm(member)

    def get_family_member(self, member_id: int) -> Optional[FamilyMemberOut]:
        member = self.repository.get_family_member(member_id)
        if member:
            return FamilyMemberOut.from_orm(member)
        return None

    def get_family_member_by_cpf(self, cpf: str) -> Optional[FamilyMemberOut]:
        member = self.repository.get_family_member_by_cpf(cpf)
        if member:
            return FamilyMemberOut.from_orm(member)
        return None

    def get_family_member_by_rg(self, rg: str) -> Optional[FamilyMemberOut]:
        member = self.repository.get_family_member_by_rg(rg)
        if member:
            return FamilyMemberOut.from_orm(member)
        return None

    def get_family_member_by_email(self, email: str) -> Optional[FamilyMemberOut]:
        member = self.repository.get_family_member_by_email(email)
        if member:
            return FamilyMemberOut.from_orm(member)
        return None

    def list_family_members(self, 
                           unit_id: Optional[int] = None,
                           main_resident_id: Optional[int] = None,
                           relationship_type: Optional[str] = None,
                           gender: Optional[str] = None,
                           marital_status: Optional[str] = None,
                           is_emergency_contact: Optional[bool] = None,
                           is_authorized_visitor: Optional[bool] = None,
                           is_resident: Optional[bool] = None) -> List[FamilyMemberOut]:
        members = self.repository.list_family_members(
            unit_id, main_resident_id, relationship_type, gender, marital_status,
            is_emergency_contact, is_authorized_visitor, is_resident
        )
        return [FamilyMemberOut.from_orm(member) for member in members]

    def search_family_members(self, search_data: FamilyMemberSearchIn) -> List[FamilyMemberOut]:
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def update_family_member(self, member_id: int, update_data: FamilyMemberUpdate, changed_by: str = "Sistema") -> Optional[FamilyMemberOut]:
        member = self.repository.update_family_member(member_id, update_data)
        if member:
            return FamilyMemberOut.from_orm(member)
        return None

    def delete_family_member(self, member_id: int) -> bool:
        return self.repository.delete_family_member(member_id)

    def get_family_member_history(self, member_id: int) -> List[FamilyMemberHistoryOut]:
        history = self.repository.get_family_member_history(member_id)
        return [FamilyMemberHistoryOut.from_orm(entry) for entry in history]

    def add_family_member_history(self, history_data: FamilyMemberHistoryIn) -> FamilyMemberHistoryOut:
        history = self.repository.add_family_member_history(history_data)
        return FamilyMemberHistoryOut.from_orm(history)

    def get_family_members_by_unit(self, unit_id: int) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_unit(unit_id)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_main_resident(self, main_resident_id: int) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_main_resident(main_resident_id)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_relationship(self, relationship_type: str) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_relationship(relationship_type)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_emergency_contacts(self, unit_id: Optional[int] = None) -> List[FamilyMemberOut]:
        members = self.repository.get_emergency_contacts(unit_id)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_authorized_visitors(self, unit_id: Optional[int] = None) -> List[FamilyMemberOut]:
        members = self.repository.get_authorized_visitors(unit_id)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_residents(self, unit_id: Optional[int] = None) -> List[FamilyMemberOut]:
        members = self.repository.get_residents(unit_id)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_age_range(self, min_age: int, max_age: int) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_age_range(min_age, max_age)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_gender(self, gender: str) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_gender(gender)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_marital_status(self, marital_status: str) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_marital_status(marital_status)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_city(self, city: str) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_city(city)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_state(self, state: str) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_state(state)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_occupation(self, occupation: str) -> List[FamilyMemberOut]:
        members = self.repository.get_family_members_by_occupation(occupation)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_recent_family_members(self, limit: int = 10) -> List[FamilyMemberOut]:
        members = self.repository.get_recent_family_members(limit)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_member_stats(self) -> FamilyMemberStatsOut:
        stats = self.repository.get_family_member_stats()
        return FamilyMemberStatsOut(**stats)

    def get_family_tree(self, main_resident_id: int) -> FamilyTreeOut:
        tree_data = self.repository.get_family_tree(main_resident_id)
        return FamilyTreeOut(**tree_data)

    def get_family_members_by_name(self, name: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(name=name)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_cpf(self, cpf: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(cpf=cpf)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_rg(self, rg: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(rg=rg)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_phone(self, phone: str) -> List[FamilyMemberOut]:
        # This would need to be implemented in the repository
        # For now, return empty list
        return []

    def get_family_members_by_email(self, email: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(email=email)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_relationship_type(self, relationship_type: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(relationship_type=relationship_type)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_gender_type(self, gender: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(gender=gender)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_marital_status_type(self, marital_status: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(marital_status=marital_status)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_emergency_contact_status(self, is_emergency_contact: bool) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(is_emergency_contact=is_emergency_contact)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_authorized_visitor_status(self, is_authorized_visitor: bool) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(is_authorized_visitor=is_authorized_visitor)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_resident_status(self, is_resident: bool) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(is_resident=is_resident)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_location(self, city: str, state: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(city=city, state=state)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    def get_family_members_by_occupation_type(self, occupation: str) -> List[FamilyMemberOut]:
        search_data = FamilyMemberSearchIn(occupation=occupation)
        members = self.repository.search_family_members(search_data)
        return [FamilyMemberOut.from_orm(member) for member in members]

    # Document methods
    def create_family_member_document(self, document_data: FamilyMemberDocumentIn) -> FamilyMemberDocumentOut:
        document = self.repository.create_family_member_document(document_data)
        return FamilyMemberDocumentOut.from_orm(document)

    def get_family_member_document(self, document_id: int) -> Optional[FamilyMemberDocumentOut]:
        document = self.repository.get_family_member_document(document_id)
        if document:
            return FamilyMemberDocumentOut.from_orm(document)
        return None

    def get_family_member_documents(self, member_id: int) -> List[FamilyMemberDocumentOut]:
        documents = self.repository.get_family_member_documents(member_id)
        return [FamilyMemberDocumentOut.from_orm(document) for document in documents]

    def update_family_member_document(self, document_id: int, update_data: dict) -> Optional[FamilyMemberDocumentOut]:
        document = self.repository.update_family_member_document(document_id, update_data)
        if document:
            return FamilyMemberDocumentOut.from_orm(document)
        return None

    def delete_family_member_document(self, document_id: int) -> bool:
        return self.repository.delete_family_member_document(document_id)

    def get_family_members_by_document_type(self, document_type: str) -> List[FamilyMemberOut]:
        # This would need to be implemented in the repository
        # For now, return empty list
        return []

    def get_family_members_by_document_number(self, document_number: str) -> List[FamilyMemberOut]:
        # This would need to be implemented in the repository
        # For now, return empty list
        return []

    def get_family_members_by_issuing_authority(self, issuing_authority: str) -> List[FamilyMemberOut]:
        # This would need to be implemented in the repository
        # For now, return empty list
        return []

    def get_family_members_by_document_expiry(self, days_ahead: int = 30) -> List[FamilyMemberOut]:
        # This would need to be implemented in the repository
        # For now, return empty list
        return []

    def get_family_members_by_document_issue_date(self, start_date: date, end_date: date) -> List[FamilyMemberOut]:
        # This would need to be implemented in the repository
        # For now, return empty list
        return []

    def get_family_members_by_document_expiry_date(self, start_date: date, end_date: date) -> List[FamilyMemberOut]:
        # This would need to be implemented in the repository
        # For now, return empty list
        return []

