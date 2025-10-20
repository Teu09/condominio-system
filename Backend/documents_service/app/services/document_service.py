from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.document_repository import DocumentRepository
from ..schemas.documents import DocumentIn, DocumentOut, DocumentUpdate, DocumentHistoryIn, DocumentApprovalIn, DocumentRejectionIn, DocumentSearchIn
from datetime import datetime
import os
import shutil
from pathlib import Path


class DocumentService:
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def create_document(self, document_data: DocumentIn, file_content: bytes) -> DocumentOut:
        # Create upload directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        file_extension = Path(document_data.file_name).suffix
        unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{document_data.file_name}"
        file_path = upload_dir / unique_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Update document data with actual file path
        document_data.file_path = str(file_path)
        
        document = self.repository.create_document(document_data)
        return DocumentOut.from_orm(document)

    def get_document(self, document_id: int) -> Optional[DocumentOut]:
        document = self.repository.get_document(document_id)
        if document:
            return DocumentOut.from_orm(document)
        return None

    def list_documents(self, 
                      document_type: Optional[str] = None,
                      status: Optional[str] = None,
                      unit_id: Optional[int] = None,
                      created_by: Optional[str] = None,
                      is_public: Optional[bool] = None) -> List[DocumentOut]:
        documents = self.repository.list_documents(document_type, status, unit_id, created_by, is_public)
        return [DocumentOut.from_orm(document) for document in documents]

    def search_documents(self, search_data: DocumentSearchIn) -> List[DocumentOut]:
        documents = self.repository.search_documents(search_data)
        return [DocumentOut.from_orm(document) for document in documents]

    def update_document(self, document_id: int, update_data: DocumentUpdate) -> Optional[DocumentOut]:
        document = self.repository.update_document(document_id, update_data)
        if document:
            return DocumentOut.from_orm(document)
        return None

    def approve_document(self, document_id: int, approval_data: DocumentApprovalIn) -> Optional[DocumentOut]:
        document = self.repository.approve_document(document_id, approval_data)
        if document:
            return DocumentOut.from_orm(document)
        return None

    def reject_document(self, document_id: int, rejection_data: DocumentRejectionIn) -> Optional[DocumentOut]:
        document = self.repository.reject_document(document_id, rejection_data)
        if document:
            return DocumentOut.from_orm(document)
        return None

    def publish_document(self, document_id: int, published_by: str) -> Optional[DocumentOut]:
        document = self.repository.publish_document(document_id, published_by)
        if document:
            return DocumentOut.from_orm(document)
        return None

    def archive_document(self, document_id: int, archived_by: str) -> Optional[DocumentOut]:
        document = self.repository.archive_document(document_id, archived_by)
        if document:
            return DocumentOut.from_orm(document)
        return None

    def download_document(self, document_id: int) -> Optional[tuple]:
        document = self.repository.get_document(document_id)
        if not document:
            return None
        
        # Increment download count
        self.repository.increment_download_count(document_id)
        
        # Check if file exists
        if not os.path.exists(document.file_path):
            return None
        
        # Read file content
        with open(document.file_path, "rb") as f:
            file_content = f.read()
        
        return file_content, document.file_name, document.mime_type

    def delete_document(self, document_id: int) -> bool:
        return self.repository.delete_document(document_id)

    def get_document_history(self, document_id: int) -> List[dict]:
        history = self.repository.get_document_history(document_id)
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

    def add_document_history(self, history_data: DocumentHistoryIn) -> dict:
        history = self.repository.add_document_history(history_data)
        return {
            "id": history.id,
            "document_id": history.document_id,
            "action": history.action,
            "description": history.description,
            "changed_by": history.changed_by,
            "old_values": history.old_values,
            "new_values": history.new_values,
            "created_at": history.created_at
        }

    def get_documents_by_type(self, document_type: str) -> List[DocumentOut]:
        documents = self.repository.get_documents_by_type(document_type)
        return [DocumentOut.from_orm(document) for document in documents]

    def get_documents_by_status(self, status: str) -> List[DocumentOut]:
        documents = self.repository.get_documents_by_status(status)
        return [DocumentOut.from_orm(document) for document in documents]

    def get_public_documents(self) -> List[DocumentOut]:
        documents = self.repository.get_public_documents()
        return [DocumentOut.from_orm(document) for document in documents]

    def get_pending_approval_documents(self) -> List[DocumentOut]:
        documents = self.repository.get_pending_approval_documents()
        return [DocumentOut.from_orm(document) for document in documents]

    def get_expired_documents(self) -> List[DocumentOut]:
        documents = self.repository.get_expired_documents()
        return [DocumentOut.from_orm(document) for document in documents]

    def get_documents_stats(self, start_date: datetime, end_date: datetime) -> dict:
        return self.repository.get_documents_stats(start_date, end_date)

    def get_documents_by_creator(self, created_by: str) -> List[DocumentOut]:
        documents = self.repository.list_documents(created_by=created_by)
        return [DocumentOut.from_orm(document) for document in documents]

    def get_documents_by_unit(self, unit_id: int) -> List[DocumentOut]:
        documents = self.repository.list_documents(unit_id=unit_id)
        return [DocumentOut.from_orm(document) for document in documents]

    def get_documents_by_tags(self, tags: List[str]) -> List[DocumentOut]:
        search_data = DocumentSearchIn(tags=tags)
        documents = self.repository.search_documents(search_data)
        return [DocumentOut.from_orm(document) for document in documents]

    def get_most_downloaded_documents(self, limit: int = 10) -> List[DocumentOut]:
        documents = self.repository.db.query(self.repository.Document).order_by(
            self.repository.Document.download_count.desc()
        ).limit(limit).all()
        return [DocumentOut.from_orm(document) for document in documents]

    def get_recent_documents(self, limit: int = 10) -> List[DocumentOut]:
        documents = self.repository.db.query(self.repository.Document).order_by(
            self.repository.Document.created_at.desc()
        ).limit(limit).all()
        return [DocumentOut.from_orm(document) for document in documents]

    def get_documents_by_date_range(self, start_date: datetime, end_date: datetime) -> List[DocumentOut]:
        search_data = DocumentSearchIn(start_date=start_date, end_date=end_date)
        documents = self.repository.search_documents(search_data)
        return [DocumentOut.from_orm(document) for document in documents]


