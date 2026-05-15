from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_admin_user, get_current_user
from models.defect_criticality import DefectCriticality
from models.user import User
from schemas.criticality import CriticalityCreate, CriticalityResponse

router = APIRouter(prefix="/criticalities", tags=["criticalities"])


@router.get("/", response_model=List[CriticalityResponse])
def get_criticalities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить список критичности"""
    return db.query(DefectCriticality).all()


@router.post("/", response_model=CriticalityResponse, status_code=201)
def create_criticality(
    crit_data: CriticalityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Создать уровень критичности"""
    existing = db.query(DefectCriticality).filter(DefectCriticality.name == crit_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Уровень критичности с таким названием уже существует")
    
    criticality = DefectCriticality(**crit_data.model_dump())
    db.add(criticality)
    db.commit()
    db.refresh(criticality)
    return criticality