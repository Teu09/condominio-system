from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.documents import DocumentIn, DocumentOut, DocumentUpdate, DocumentHistoryIn, DocumentApprovalIn, DocumentRejectionIn, DocumentSearchIn
from ..services.document_service import DocumentService
from datetime import datetime
import os

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentOut)
def create_document(
    title: str = Form(...),
    description: str = Form(...),
    document_type: str = Form(...),
    version: str = Form("1.0"),
    is_public: bool = Form(True),
    requires_approval: bool = Form(False),
    expires_at: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    unit_id: Optional[int] = Form(None),
    created_by: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    
    # Validate file size (10MB limit)
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máximo 10MB")
    
    # Read file content
    file_content = file.file.read()
    
    # Parse tags
    tags_list = None
    if tags:
        tags_list = [tag.strip() for tag in tags.split(",")]
    
    # Parse expires_at
    expires_at_dt = None
    if expires_at:
        try:
            expires_at_dt = datetime.fromisoformat(expires_at)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido")
    
    document_data = DocumentIn(
        title=title,
        description=description,
        document_type=document_type,
        file_name=file.filename,
        file_size=file.size,
        mime_type=file.content_type,
        version=version,
        is_public=is_public,
        requires_approval=requires_approval,
        expires_at=expires_at_dt,
        tags=tags_list,
        unit_id=unit_id,
        created_by=created_by
    )
    
    return service.create_document(document_data, file_content)


@router.get("/", response_model=List[DocumentOut])
def list_documents(
    document_type: Optional[str] = None,
    status: Optional[str] = None,
    unit_id: Optional[int] = None,
    created_by: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.list_documents(document_type, status, unit_id, created_by, is_public)


@router.post("/search", response_model=List[DocumentOut])
def search_documents(
    search_data: DocumentSearchIn,
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.search_documents(search_data)


@router.get("/{document_id}", response_model=DocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    document = service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document


@router.get("/{document_id}/download")
def download_document(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    result = service.download_document(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    
    file_content, file_name, mime_type = result
    
    from fastapi.responses import Response
    return Response(
        content=file_content,
        media_type=mime_type,
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )


@router.put("/{document_id}", response_model=DocumentOut)
def update_document(
    document_id: int,
    update_data: DocumentUpdate,
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    document = service.update_document(document_id, update_data)
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document


@router.post("/{document_id}/approve", response_model=DocumentOut)
def approve_document(
    document_id: int,
    approval_data: DocumentApprovalIn,
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    document = service.approve_document(document_id, approval_data)
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document


@router.post("/{document_id}/reject", response_model=DocumentOut)
def reject_document(
    document_id: int,
    rejection_data: DocumentRejectionIn,
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    document = service.reject_document(document_id, rejection_data)
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document


@router.post("/{document_id}/publish", response_model=DocumentOut)
def publish_document(
    document_id: int,
    published_by: str,
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    document = service.publish_document(document_id, published_by)
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document


@router.post("/{document_id}/archive", response_model=DocumentOut)
def archive_document(
    document_id: int,
    archived_by: str,
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    document = service.archive_document(document_id, archived_by)
    if not document:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return document


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    success = service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return {"message": "Documento excluído com sucesso"}


@router.get("/{document_id}/history")
def get_document_history(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_document_history(document_id)


@router.post("/{document_id}/history", response_model=dict)
def add_document_history(
    document_id: int,
    history_data: DocumentHistoryIn,
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    history_data.document_id = document_id
    return service.add_document_history(history_data)


@router.get("/type/{document_type}")
def get_documents_by_type(document_type: str, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_documents_by_type(document_type)


@router.get("/status/{status}")
def get_documents_by_status(status: str, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_documents_by_status(status)


@router.get("/public/list")
def get_public_documents(db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_public_documents()


@router.get("/pending/list")
def get_pending_approval_documents(db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_pending_approval_documents()


@router.get("/expired/list")
def get_expired_documents(db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_expired_documents()


@router.get("/creator/{created_by}")
def get_documents_by_creator(created_by: str, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_documents_by_creator(created_by)


@router.get("/unit/{unit_id}")
def get_documents_by_unit(unit_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_documents_by_unit(unit_id)


@router.get("/tags/{tags}")
def get_documents_by_tags(tags: str, db: Session = Depends(get_db)):
    service = DocumentService(db)
    tags_list = [tag.strip() for tag in tags.split(",")]
    return service.get_documents_by_tags(tags_list)


@router.get("/most-downloaded/list")
def get_most_downloaded_documents(limit: int = 10, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_most_downloaded_documents(limit)


@router.get("/recent/list")
def get_recent_documents(limit: int = 10, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_recent_documents(limit)


@router.get("/stats/summary")
def get_documents_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = DocumentService(db)
    return service.get_documents_stats(start, end)


