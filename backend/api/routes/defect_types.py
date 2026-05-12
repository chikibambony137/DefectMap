from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_admin_user
from models.defect_type import DefectType
from models.user import User
from schemas.defect_type import DefectTypeCreate, DefectTypeUpdate, DefectTypeResponse

router = APIRouter(prefix="/defect-types", tags=["defect_types"])


@router.get("/", response_model=List[DefectTypeResponse])
def get_defect_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Получить список типов дефектов"""
    return db.query(DefectType).all()


@router.post("/", response_model=DefectTypeResponse, status_code=201)
def create_defect_type(
    type_data: DefectTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Создать тип дефекта"""
    existing = db.query(DefectType).filter(DefectType.name == type_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Тип дефекта с таким названием уже существует")
    
    defect_type = DefectType(**type_data.model_dump())
    db.add(defect_type)
    db.commit()
    db.refresh(defect_type)
    return defect_type


@router.put("/{type_id}", response_model=DefectTypeResponse)
def update_defect_type(
    type_id: int,
    type_data: DefectTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Обновить тип дефекта"""
    defect_type = db.query(DefectType).filter(DefectType.id == type_id).first()
    if not defect_type:
        raise HTTPException(status_code=404, detail="Тип дефекта не найден")
    
    update_data = type_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(defect_type, field, value)
    
    db.commit()
    db.refresh(defect_type)
    return defect_type