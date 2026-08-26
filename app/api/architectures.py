import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.api.schemas import ArchRequest, ArchResponse, CompareRequest
from app.models.architecture import ArchitectureRequest
from app.services.architect import ArchitectureEngine

router = APIRouter()

@router.post("/generate", response_model=ArchResponse, status_code=201)
async def generate_architecture(payload: ArchRequest, db: AsyncSession = Depends(get_db)):
    engine = ArchitectureEngine(db)
    return await engine.generate(payload.requirement, payload.constraints)

@router.post("/compare")
async def compare_approaches(payload: CompareRequest, db: AsyncSession = Depends(get_db)):
    engine = ArchitectureEngine(db)
    return await engine.compare_approaches(payload.requirement, payload.approaches)

@router.get("", response_model=List[ArchResponse])
async def list_requests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ArchitectureRequest).order_by(ArchitectureRequest.created_at.desc()))
    return result.scalars().all()

@router.get("/{req_id}", response_model=ArchResponse)
async def get_request(req_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ArchitectureRequest).where(ArchitectureRequest.id == req_id))
    req = result.scalar_one_or_none()
    if not req:
        raise HTTPException(404, "Request not found")
    return req
