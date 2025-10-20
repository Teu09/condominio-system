from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, extract
from typing import List, Optional, Dict, Any
from ..models.family_members import FamilyMember, FamilyMemberHistory, FamilyMemberDocument
from ..schemas.family_members import FamilyMemberIn, FamilyMemberUpdate, FamilyMemberHistoryIn, FamilyMemberSearchIn, FamilyMemberDocumentIn
from datetime import datetime, date
import json


class FamilyMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_family_member(self, member_data: FamilyMemberIn) -> FamilyMember:
        db_member = FamilyMember(
            name=member_data.name,
            cpf=member_data.cpf,
            rg=member_data.rg,
            birth_date=member_data.birth_date,
            gender=member_data.gender,
            marital_status=member_data.marital_status,
            relationship_type=member_data.relationship_type,
            phone=member_data.phone,
            email=member_data.email,
            address=member_data.address,
            city=member_data.city,
            state=member_data.state,
            zip_code=member_data.zip_code,
            occupation=member_data.occupation,
            employer=member_data.employer,
            emergency_contact_name=member_data.emergency_contact_name,
            emergency_contact_phone=member_data.emergency_contact_phone,
            emergency_contact_relationship=member_data.emergency_contact_relationship,
            is_emergency_contact=member_data.is_emergency_contact,
            is_authorized_visitor=member_data.is_authorized_visitor,
            is_resident=member_data.is_resident,
            notes=member_data.notes,
            unit_id=member_data.unit_id,
            main_resident_id=member_data.main_resident_id,
            created_by=member_data.created_by
        )
        
        self.db.add(db_member)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = FamilyMemberHistory(
            member_id=db_member.id,
            action="created",
            description="Membro da família criado",
            changed_by=member_data.created_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_member)
        return db_member

    def get_family_member(self, member_id: int) -> Optional[FamilyMember]:
        return self.db.query(FamilyMember).filter(FamilyMember.id == member_id).first()

    def get_family_member_by_cpf(self, cpf: str) -> Optional[FamilyMember]:
        return self.db.query(FamilyMember).filter(FamilyMember.cpf == cpf).first()

    def get_family_member_by_rg(self, rg: str) -> Optional[FamilyMember]:
        return self.db.query(FamilyMember).filter(FamilyMember.rg == rg).first()

    def get_family_member_by_email(self, email: str) -> Optional[FamilyMember]:
        return self.db.query(FamilyMember).filter(FamilyMember.email == email).first()

    def list_family_members(self, 
                           unit_id: Optional[int] = None,
                           main_resident_id: Optional[int] = None,
                           relationship_type: Optional[str] = None,
                           gender: Optional[str] = None,
                           marital_status: Optional[str] = None,
                           is_emergency_contact: Optional[bool] = None,
                           is_authorized_visitor: Optional[bool] = None,
                           is_resident: Optional[bool] = None) -> List[FamilyMember]:
        query = self.db.query(FamilyMember)
        
        if unit_id:
            query = query.filter(FamilyMember.unit_id == unit_id)
        if main_resident_id:
            query = query.filter(FamilyMember.main_resident_id == main_resident_id)
        if relationship_type:
            query = query.filter(FamilyMember.relationship_type == relationship_type)
        if gender:
            query = query.filter(FamilyMember.gender == gender)
        if marital_status:
            query = query.filter(FamilyMember.marital_status == marital_status)
        if is_emergency_contact is not None:
            query = query.filter(FamilyMember.is_emergency_contact == is_emergency_contact)
        if is_authorized_visitor is not None:
            query = query.filter(FamilyMember.is_authorized_visitor == is_authorized_visitor)
        if is_resident is not None:
            query = query.filter(FamilyMember.is_resident == is_resident)
            
        return query.order_by(desc(FamilyMember.created_at)).all()

    def search_family_members(self, search_data: FamilyMemberSearchIn) -> List[FamilyMember]:
        query = self.db.query(FamilyMember)
        
        if search_data.name:
            query = query.filter(FamilyMember.name.ilike(f"%{search_data.name}%"))
        if search_data.cpf:
            query = query.filter(FamilyMember.cpf == search_data.cpf)
        if search_data.rg:
            query = query.filter(FamilyMember.rg == search_data.rg)
        if search_data.relationship_type:
            query = query.filter(FamilyMember.relationship_type == search_data.relationship_type)
        if search_data.gender:
            query = query.filter(FamilyMember.gender == search_data.gender)
        if search_data.marital_status:
            query = query.filter(FamilyMember.marital_status == search_data.marital_status)
        if search_data.is_emergency_contact is not None:
            query = query.filter(FamilyMember.is_emergency_contact == search_data.is_emergency_contact)
        if search_data.is_authorized_visitor is not None:
            query = query.filter(FamilyMember.is_authorized_visitor == search_data.is_authorized_visitor)
        if search_data.is_resident is not None:
            query = query.filter(FamilyMember.is_resident == search_data.is_resident)
        if search_data.unit_id:
            query = query.filter(FamilyMember.unit_id == search_data.unit_id)
        if search_data.main_resident_id:
            query = query.filter(FamilyMember.main_resident_id == search_data.main_resident_id)
        if search_data.city:
            query = query.filter(FamilyMember.city.ilike(f"%{search_data.city}%"))
        if search_data.state:
            query = query.filter(FamilyMember.state == search_data.state)
        if search_data.occupation:
            query = query.filter(FamilyMember.occupation.ilike(f"%{search_data.occupation}%"))
            
        return query.order_by(desc(FamilyMember.created_at)).all()

    def update_family_member(self, member_id: int, update_data: FamilyMemberUpdate) -> Optional[FamilyMember]:
        db_member = self.get_family_member(member_id)
        if not db_member:
            return None
        
        # Store old values for history
        old_values = {
            "name": db_member.name,
            "phone": db_member.phone,
            "email": db_member.email,
            "address": db_member.address,
            "is_emergency_contact": db_member.is_emergency_contact,
            "is_authorized_visitor": db_member.is_authorized_visitor,
            "is_resident": db_member.is_resident
        }
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_member, field, value)
        
        db_member.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "name": db_member.name,
            "phone": db_member.phone,
            "email": db_member.email,
            "address": db_member.address,
            "is_emergency_contact": db_member.is_emergency_contact,
            "is_authorized_visitor": db_member.is_authorized_visitor,
            "is_resident": db_member.is_resident
        }
        
        # Add history entry
        history_entry = FamilyMemberHistory(
            member_id=member_id,
            action="updated",
            description=f"Membro da família atualizado: {', '.join(update_dict.keys())}",
            changed_by="Sistema",
            old_values=json.dumps(old_values),
            new_values=json.dumps(new_values)
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_member)
        return db_member

    def delete_family_member(self, member_id: int) -> bool:
        db_member = self.get_family_member(member_id)
        if not db_member:
            return False
        
        self.db.delete(db_member)
        self.db.commit()
        return True

    def get_family_member_history(self, member_id: int) -> List[FamilyMemberHistory]:
        return self.db.query(FamilyMemberHistory).filter(
            FamilyMemberHistory.member_id == member_id
        ).order_by(desc(FamilyMemberHistory.created_at)).all()

    def add_family_member_history(self, history_data: FamilyMemberHistoryIn) -> FamilyMemberHistory:
        db_history = FamilyMemberHistory(
            member_id=history_data.member_id,
            action=history_data.action,
            description=history_data.description,
            changed_by=history_data.changed_by,
            old_values=json.dumps(history_data.old_values) if history_data.old_values else None,
            new_values=json.dumps(history_data.new_values) if history_data.new_values else None
        )
        
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def get_family_members_by_unit(self, unit_id: int) -> List[FamilyMember]:
        return self.db.query(FamilyMember).filter(
            FamilyMember.unit_id == unit_id
        ).order_by(desc(FamilyMember.created_at)).all()

    def get_family_members_by_main_resident(self, main_resident_id: int) -> List[FamilyMember]:
        return self.db.query(FamilyMember).filter(
            FamilyMember.main_resident_id == main_resident_id
        ).order_by(desc(FamilyMember.created_at)).all()

    def get_family_members_by_relationship(self, relationship_type: str) -> List[FamilyMember]:
        return self.db.query(FamilyMember).filter(
            FamilyMember.relationship_type == relationship_type
        ).order_by(desc(FamilyMember.created_at)).all()

    def get_emergency_contacts(self, unit_id: Optional[int] = None) -> List[FamilyMember]:
        query = self.db.query(FamilyMember).filter(FamilyMember.is_emergency_contact == True)
        if unit_id:
            query = query.filter(FamilyMember.unit_id == unit_id)
        return query.order_by(desc(FamilyMember.created_at)).all()

    def get_authorized_visitors(self, unit_id: Optional[int] = None) -> List[FamilyMember]:
        query = self.db.query(FamilyMember).filter(FamilyMember.is_authorized_visitor == True)
        if unit_id:
            query = query.filter(FamilyMember.unit_id == unit_id)
        return query.order_by(desc(FamilyMember.created_at)).all()

    def get_residents(self, unit_id: Optional[int] = None) -> List[FamilyMember]:
        query = self.db.query(FamilyMember).filter(FamilyMember.is_resident == True)
        if unit_id:
            query = query.filter(FamilyMember.unit_id == unit_id)
        return query.order_by(desc(FamilyMember.created_at)).all()

    def get_family_members_by_age_range(self, min_age: int, max_age: int) -> List[FamilyMember]:
        current_date = date.today()
        min_birth_date = date(current_date.year - max_age, current_date.month, current_date.day)
        max_birth_date = date(current_date.year - min_age, current_date.month, current_date.day)
        
        return self.db.query(FamilyMember).filter(
            and_(
                FamilyMember.birth_date >= min_birth_date,
                FamilyMember.birth_date <= max_birth_date
            )
        ).order_by(desc(FamilyMember.birth_date)).all()

    def get_family_members_by_gender(self, gender: str) -> List[FamilyMember]:
        return self.db.query(FamilyMember).filter(
            FamilyMember.gender == gender
        ).order_by(desc(FamilyMember.created_at)).all()

    def get_family_members_by_marital_status(self, marital_status: str) -> List[FamilyMember]:
        return self.db.query(FamilyMember).filter(
            FamilyMember.marital_status == marital_status
        ).order_by(desc(FamilyMember.created_at)).all()

    def get_family_members_by_city(self, city: str) -> List[FamilyMember]:
        return self.db.query(FamilyMember).filter(
            FamilyMember.city.ilike(f"%{city}%")
        ).order_by(desc(FamilyMember.created_at)).all()

    def get_family_members_by_state(self, state: str) -> List[FamilyMember]:
        return self.db.query(FamilyMember).filter(
            FamilyMember.state == state
        ).order_by(desc(FamilyMember.created_at)).all()

    def get_family_members_by_occupation(self, occupation: str) -> List[FamilyMember]:
        return self.db.query(FamilyMember).filter(
            FamilyMember.occupation.ilike(f"%{occupation}%")
        ).order_by(desc(FamilyMember.created_at)).all()

    def get_recent_family_members(self, limit: int = 10) -> List[FamilyMember]:
        return self.db.query(FamilyMember).order_by(
            desc(FamilyMember.created_at)
        ).limit(limit).all()

    def get_family_member_stats(self) -> Dict[str, Any]:
        total_members = self.db.query(FamilyMember).count()
        
        residents = self.db.query(FamilyMember).filter(FamilyMember.is_resident == True).count()
        non_residents = total_members - residents
        
        emergency_contacts = self.db.query(FamilyMember).filter(FamilyMember.is_emergency_contact == True).count()
        authorized_visitors = self.db.query(FamilyMember).filter(FamilyMember.is_authorized_visitor == True).count()
        
        # Relationship breakdown
        relationship_breakdown = {}
        relationship_counts = self.db.query(
            FamilyMember.relationship_type, 
            func.count(FamilyMember.id)
        ).group_by(FamilyMember.relationship_type).all()
        
        for relationship, count in relationship_counts:
            relationship_breakdown[relationship] = count
        
        # Gender breakdown
        gender_breakdown = {}
        gender_counts = self.db.query(
            FamilyMember.gender, 
            func.count(FamilyMember.id)
        ).group_by(FamilyMember.gender).all()
        
        for gender, count in gender_counts:
            gender_breakdown[gender] = count
        
        # Marital status breakdown
        marital_status_breakdown = {}
        marital_status_counts = self.db.query(
            FamilyMember.marital_status, 
            func.count(FamilyMember.id)
        ).group_by(FamilyMember.marital_status).all()
        
        for marital_status, count in marital_status_counts:
            marital_status_breakdown[marital_status] = count
        
        # Age breakdown
        age_breakdown = {}
        current_date = date.today()
        
        # Calculate age groups
        age_groups = [
            (0, 12, "0-12"),
            (13, 17, "13-17"),
            (18, 25, "18-25"),
            (26, 35, "26-35"),
            (36, 50, "36-50"),
            (51, 65, "51-65"),
            (66, 100, "66+")
        ]
        
        for min_age, max_age, group_name in age_groups:
            min_birth_date = date(current_date.year - max_age, current_date.month, current_date.day)
            max_birth_date = date(current_date.year - min_age, current_date.month, current_date.day)
            
            count = self.db.query(FamilyMember).filter(
                and_(
                    FamilyMember.birth_date >= min_birth_date,
                    FamilyMember.birth_date <= max_birth_date
                )
            ).count()
            
            age_breakdown[group_name] = count
        
        # Unit breakdown
        unit_breakdown = {}
        unit_counts = self.db.query(
            FamilyMember.unit_id, 
            func.count(FamilyMember.id)
        ).group_by(FamilyMember.unit_id).all()
        
        for unit_id, count in unit_counts:
            unit_breakdown[str(unit_id)] = count
        
        # Recent members
        recent_members = self.get_recent_family_members(5)
        recent_data = [
            {
                "id": member.id,
                "name": member.name,
                "relationship_type": member.relationship_type,
                "created_at": member.created_at
            }
            for member in recent_members
        ]
        
        # Members by relationship
        members_by_relationship = {}
        for relationship in relationship_breakdown.keys():
            members = self.db.query(FamilyMember).filter(
                FamilyMember.relationship_type == relationship
            ).all()
            members_by_relationship[relationship] = [
                {
                    "id": member.id,
                    "name": member.name,
                    "unit_id": member.unit_id
                }
                for member in members
            ]
        
        return {
            "total_members": total_members,
            "residents": residents,
            "non_residents": non_residents,
            "emergency_contacts": emergency_contacts,
            "authorized_visitors": authorized_visitors,
            "relationship_breakdown": relationship_breakdown,
            "gender_breakdown": gender_breakdown,
            "marital_status_breakdown": marital_status_breakdown,
            "age_breakdown": age_breakdown,
            "unit_breakdown": unit_breakdown,
            "recent_members": recent_data,
            "members_by_relationship": members_by_relationship
        }

    def get_family_tree(self, main_resident_id: int) -> Dict[str, Any]:
        # Get main resident
        main_resident = self.db.query(FamilyMember).filter(
            FamilyMember.main_resident_id == main_resident_id,
            FamilyMember.is_resident == True
        ).first()
        
        if not main_resident:
            return {"main_resident": None, "family_members": [], "relationships": []}
        
        # Get all family members
        family_members = self.db.query(FamilyMember).filter(
            FamilyMember.main_resident_id == main_resident_id
        ).all()
        
        # Build relationships
        relationships = []
        for member in family_members:
            relationships.append({
                "from": main_resident_id,
                "to": member.id,
                "relationship": member.relationship_type
            })
        
        return {
            "main_resident": {
                "id": main_resident.id,
                "name": main_resident.name,
                "relationship_type": main_resident.relationship_type
            },
            "family_members": [
                {
                    "id": member.id,
                    "name": member.name,
                    "relationship_type": member.relationship_type,
                    "is_resident": member.is_resident,
                    "is_emergency_contact": member.is_emergency_contact,
                    "is_authorized_visitor": member.is_authorized_visitor
                }
                for member in family_members
            ],
            "relationships": relationships
        }

    # Document methods
    def create_family_member_document(self, document_data: FamilyMemberDocumentIn) -> FamilyMemberDocument:
        db_document = FamilyMemberDocument(
            member_id=document_data.member_id,
            document_type=document_data.document_type,
            document_number=document_data.document_number,
            issuing_authority=document_data.issuing_authority,
            issue_date=document_data.issue_date,
            expiry_date=document_data.expiry_date,
            file_path=document_data.file_path,
            notes=document_data.notes
        )
        
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def get_family_member_document(self, document_id: int) -> Optional[FamilyMemberDocument]:
        return self.db.query(FamilyMemberDocument).filter(FamilyMemberDocument.id == document_id).first()

    def get_family_member_documents(self, member_id: int) -> List[FamilyMemberDocument]:
        return self.db.query(FamilyMemberDocument).filter(
            FamilyMemberDocument.member_id == member_id
        ).order_by(desc(FamilyMemberDocument.created_at)).all()

    def update_family_member_document(self, document_id: int, update_data: dict) -> Optional[FamilyMemberDocument]:
        db_document = self.get_family_member_document(document_id)
        if not db_document:
            return None
        
        for field, value in update_data.items():
            setattr(db_document, field, value)
        
        db_document.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def delete_family_member_document(self, document_id: int) -> bool:
        db_document = self.get_family_member_document(document_id)
        if not db_document:
            return False
        
        self.db.delete(db_document)
        self.db.commit()
        return True

