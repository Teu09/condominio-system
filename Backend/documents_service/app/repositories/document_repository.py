from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.documents import Document, DocumentHistory
from ..schemas.documents import DocumentIn, DocumentUpdate, DocumentHistoryIn, DocumentApprovalIn, DocumentRejectionIn, DocumentSearchIn
from datetime import datetime
import os


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, document_data: DocumentIn) -> Document:
        db_document = Document(
            title=document_data.title,
            description=document_data.description,
            document_type=document_data.document_type,
            file_path=document_data.file_path,
            file_name=document_data.file_name,
            file_size=document_data.file_size,
            mime_type=document_data.mime_type,
            version=document_data.version,
            is_public=document_data.is_public,
            requires_approval=document_data.requires_approval,
            expires_at=document_data.expires_at,
            tags=document_data.tags,
            unit_id=document_data.unit_id,
            created_by=document_data.created_by
        )
        
        self.db.add(db_document)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = DocumentHistory(
            document_id=db_document.id,
            action="created",
            description="Documento criado",
            changed_by=document_data.created_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def get_document(self, document_id: int) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def list_documents(self, 
                      document_type: Optional[str] = None,
                      status: Optional[str] = None,
                      unit_id: Optional[int] = None,
                      created_by: Optional[str] = None,
                      is_public: Optional[bool] = None) -> List[Document]:
        query = self.db.query(Document)
        
        if document_type:
            query = query.filter(Document.document_type == document_type)
        if status:
            query = query.filter(Document.status == status)
        if unit_id:
            query = query.filter(Document.unit_id == unit_id)
        if created_by:
            query = query.filter(Document.created_by == created_by)
        if is_public is not None:
            query = query.filter(Document.is_public == is_public)
            
        return query.order_by(Document.created_at.desc()).all()

    def search_documents(self, search_data: DocumentSearchIn) -> List[Document]:
        query = self.db.query(Document)
        
        if search_data.query:
            query = query.filter(
                (Document.title.ilike(f"%{search_data.query}%")) |
                (Document.description.ilike(f"%{search_data.query}%")) |
                (Document.file_name.ilike(f"%{search_data.query}%"))
            )
        
        if search_data.document_type:
            query = query.filter(Document.document_type == search_data.document_type)
        
        if search_data.status:
            query = query.filter(Document.status == search_data.status)
        
        if search_data.unit_id:
            query = query.filter(Document.unit_id == search_data.unit_id)
        
        if search_data.created_by:
            query = query.filter(Document.created_by == search_data.created_by)
        
        if search_data.start_date:
            query = query.filter(Document.created_at >= search_data.start_date)
        
        if search_data.end_date:
            query = query.filter(Document.created_at <= search_data.end_date)
        
        if search_data.tags:
            for tag in search_data.tags:
                query = query.filter(Document.tags.contains([tag]))
        
        return query.order_by(Document.created_at.desc()).all()

    def update_document(self, document_id: int, update_data: DocumentUpdate) -> Optional[Document]:
        db_document = self.get_document(document_id)
        if not db_document:
            return None
        
        # Store old values for history
        old_values = {
            "title": db_document.title,
            "description": db_document.description,
            "document_type": db_document.document_type,
            "version": db_document.version,
            "status": db_document.status,
            "is_public": db_document.is_public
        }
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_document, field, value)
        
        db_document.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "title": db_document.title,
            "description": db_document.description,
            "document_type": db_document.document_type,
            "version": db_document.version,
            "status": db_document.status,
            "is_public": db_document.is_public
        }
        
        # Add history entry
        history_entry = DocumentHistory(
            document_id=document_id,
            action="updated",
            description=f"Documento atualizado: {', '.join(update_dict.keys())}",
            changed_by="Sistema",
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def approve_document(self, document_id: int, approval_data: DocumentApprovalIn) -> Optional[Document]:
        db_document = self.get_document(document_id)
        if not db_document:
            return None
        
        # Store old values for history
        old_values = {"status": db_document.status}
        
        db_document.status = "approved"
        db_document.approved_by = approval_data.approved_by
        db_document.approved_at = datetime.utcnow()
        db_document.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_document.status}
        
        # Add history entry
        history_entry = DocumentHistory(
            document_id=document_id,
            action="approved",
            description=f"Documento aprovado{f' - {approval_data.comments}' if approval_data.comments else ''}",
            changed_by=approval_data.approved_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def reject_document(self, document_id: int, rejection_data: DocumentRejectionIn) -> Optional[Document]:
        db_document = self.get_document(document_id)
        if not db_document:
            return None
        
        # Store old values for history
        old_values = {"status": db_document.status}
        
        db_document.status = "rejected"
        db_document.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_document.status}
        
        # Add history entry
        history_entry = DocumentHistory(
            document_id=document_id,
            action="rejected",
            description=f"Documento rejeitado: {rejection_data.reason}{f' - {rejection_data.comments}' if rejection_data.comments else ''}",
            changed_by=rejection_data.rejected_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def publish_document(self, document_id: int, published_by: str) -> Optional[Document]:
        db_document = self.get_document(document_id)
        if not db_document:
            return None
        
        # Store old values for history
        old_values = {"status": db_document.status}
        
        db_document.status = "published"
        db_document.published_at = datetime.utcnow()
        db_document.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_document.status}
        
        # Add history entry
        history_entry = DocumentHistory(
            document_id=document_id,
            action="published",
            description="Documento publicado",
            changed_by=published_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def archive_document(self, document_id: int, archived_by: str) -> Optional[Document]:
        db_document = self.get_document(document_id)
        if not db_document:
            return None
        
        # Store old values for history
        old_values = {"status": db_document.status}
        
        db_document.status = "archived"
        db_document.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_document.status}
        
        # Add history entry
        history_entry = DocumentHistory(
            document_id=document_id,
            action="archived",
            description="Documento arquivado",
            changed_by=archived_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def increment_download_count(self, document_id: int) -> Optional[Document]:
        db_document = self.get_document(document_id)
        if not db_document:
            return None
        
        db_document.download_count += 1
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def delete_document(self, document_id: int) -> bool:
        db_document = self.get_document(document_id)
        if not db_document:
            return False
        
        # Delete physical file
        if os.path.exists(db_document.file_path):
            os.remove(db_document.file_path)
        
        self.db.delete(db_document)
        self.db.commit()
        return True

    def get_document_history(self, document_id: int) -> List[DocumentHistory]:
        return self.db.query(DocumentHistory).filter(
            DocumentHistory.document_id == document_id
        ).order_by(DocumentHistory.created_at.desc()).all()

    def add_document_history(self, history_data: DocumentHistoryIn) -> DocumentHistory:
        db_history = DocumentHistory(
            document_id=history_data.document_id,
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

    def get_documents_by_type(self, document_type: str) -> List[Document]:
        return self.db.query(Document).filter(
            Document.document_type == document_type
        ).order_by(Document.created_at.desc()).all()

    def get_documents_by_status(self, status: str) -> List[Document]:
        return self.db.query(Document).filter(
            Document.status == status
        ).order_by(Document.created_at.desc()).all()

    def get_public_documents(self) -> List[Document]:
        return self.db.query(Document).filter(
            Document.is_public == True,
            Document.status == "published"
        ).order_by(Document.created_at.desc()).all()

    def get_pending_approval_documents(self) -> List[Document]:
        return self.db.query(Document).filter(
            Document.status == "pending_approval"
        ).order_by(Document.created_at.asc()).all()

    def get_expired_documents(self) -> List[Document]:
        return self.db.query(Document).filter(
            Document.expires_at < datetime.utcnow(),
            Document.status != "archived"
        ).order_by(Document.expires_at.asc()).all()

    def get_documents_stats(self, start_date: datetime, end_date: datetime) -> dict:
        query = self.db.query(Document).filter(
            Document.created_at >= start_date,
            Document.created_at <= end_date
        )
        
        total_documents = query.count()
        
        type_breakdown = {}
        status_breakdown = {}
        
        for document in query.all():
            type_breakdown[document.document_type] = type_breakdown.get(document.document_type, 0) + 1
            status_breakdown[document.status] = status_breakdown.get(document.status, 0) + 1
        
        return {
            "total_documents": total_documents,
            "type_breakdown": type_breakdown,
            "status_breakdown": status_breakdown
        }


