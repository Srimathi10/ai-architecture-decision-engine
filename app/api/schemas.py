from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

class ArchRequest(BaseModel):
    requirement: str
    constraints: Dict[str, Any] = {}

class ArchResponse(BaseModel):
    id: str
    requirement: str
    constraints: Dict[str, Any]
    status: str
    result: Dict[str, Any]
    created_at: datetime
    completed_at: Optional[datetime]
    class Config:
        from_attributes = True

class CompareRequest(BaseModel):
    requirement: str
    approaches: List[str]
