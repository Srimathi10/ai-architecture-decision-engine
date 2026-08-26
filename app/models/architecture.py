import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, JSON, Text
from app.core.database import Base

class ArchStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"

class ArchitectureRequest(Base):
    __tablename__ = "architecture_requests"
    id = Column(String(36), primary_key=True)
    requirement = Column(Text, nullable=False)
    constraints = Column(JSON, default=dict)
    status = Column(Enum(ArchStatus), default=ArchStatus.PENDING)
    result = Column(JSON, default=dict)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
