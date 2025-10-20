from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ReportRequest(BaseModel):
    report_type: str  # visitors, maintenance, reservations, financial
    start_date: datetime
    end_date: datetime
    filters: Optional[Dict[str, Any]] = {}


class ReportOut(BaseModel):
    id: int
    report_type: str
    title: str
    generated_at: datetime
    data: Dict[str, Any]
    summary: Dict[str, Any]














