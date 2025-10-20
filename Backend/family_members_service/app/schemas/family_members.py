from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class RelationshipType(str, Enum):
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    SIBLING = "sibling"
    GRANDPARENT = "grandparent"
    GRANDCHILD = "grandchild"
    UNCLE_AUNT = "uncle_aunt"
    NEPHEW_NIECE = "nephew_niece"
    COUSIN = "cousin"
    IN_LAW = "in_law"
    OTHER = "other"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class MaritalStatus(str, Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    SEPARATED = "separated"
    OTHER = "other"


class FamilyMemberIn(BaseModel):
    name: str
    cpf: str
    rg: Optional[str] = None
    birth_date: date
    gender: Gender
    marital_status: MaritalStatus
    relationship_type: RelationshipType
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    occupation: Optional[str] = None
    employer: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    is_emergency_contact: bool = False
    is_authorized_visitor: bool = False
    is_resident: bool = False
    notes: Optional[str] = None
    unit_id: int
    main_resident_id: int
    created_by: str


class FamilyMemberOut(BaseModel):
    id: int
    name: str
    cpf: str
    rg: Optional[str]
    birth_date: date
    gender: Gender
    marital_status: MaritalStatus
    relationship_type: RelationshipType
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    occupation: Optional[str]
    employer: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    emergency_contact_relationship: Optional[str]
    is_emergency_contact: bool
    is_authorized_visitor: bool
    is_resident: bool
    notes: Optional[str]
    unit_id: int
    main_resident_id: int
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FamilyMemberUpdate(BaseModel):
    name: Optional[str] = None
    rg: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    relationship_type: Optional[RelationshipType] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    occupation: Optional[str] = None
    employer: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    is_emergency_contact: Optional[bool] = None
    is_authorized_visitor: Optional[bool] = None
    is_resident: Optional[bool] = None
    notes: Optional[str] = None


class FamilyMemberHistoryIn(BaseModel):
    member_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None


class FamilyMemberHistoryOut(BaseModel):
    id: int
    member_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict]
    new_values: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class FamilyMemberSearchIn(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    relationship_type: Optional[RelationshipType] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    is_emergency_contact: Optional[bool] = None
    is_authorized_visitor: Optional[bool] = None
    is_resident: Optional[bool] = None
    unit_id: Optional[int] = None
    main_resident_id: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    occupation: Optional[str] = None


class FamilyMemberStatsOut(BaseModel):
    total_members: int
    residents: int
    non_residents: int
    emergency_contacts: int
    authorized_visitors: int
    relationship_breakdown: dict
    gender_breakdown: dict
    marital_status_breakdown: dict
    age_breakdown: dict
    unit_breakdown: dict
    recent_members: List[dict]
    members_by_relationship: dict


class FamilyTreeOut(BaseModel):
    main_resident: dict
    family_members: List[dict]
    relationships: List[dict]


class FamilyMemberDocumentIn(BaseModel):
    member_id: int
    document_type: str
    document_number: str
    issuing_authority: str
    issue_date: date
    expiry_date: Optional[date] = None
    file_path: Optional[str] = None
    notes: Optional[str] = None


class FamilyMemberDocumentOut(BaseModel):
    id: int
    member_id: int
    document_type: str
    document_number: str
    issuing_authority: str
    issue_date: date
    expiry_date: Optional[date]
    file_path: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

