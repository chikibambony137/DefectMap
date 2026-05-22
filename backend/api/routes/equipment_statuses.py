from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.equipment_status import EquipmentStatus
from schemas.equipment_status import (EquipmentStatusCreate,
                                      EquipmentStatusResponse)

router = APIRouter(prefix="/equipment-statuses", tags=["equipment-statuses"])


@router.get("/", response_model=List[EquipmentStatusResponse])
def get_equipment_statuses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(EquipmentStatus).all()


@router.post("/", response_model=EquipmentStatusResponse, status_code=201)
def create_equipment_status(
    data: EquipmentStatusCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    existing = db.query(EquipmentStatus).filter(
        EquipmentStatus.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400,
                            detail="Статус с таким именем уже существует")
    status = EquipmentStatus(**data.model_dump())
    db.add(status)
    db.commit()
    db.refresh(status)
    return status


@router.delete("/{status_id}", status_code=204)
def delete_equipment_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    status = db.query(EquipmentStatus).filter(
        EquipmentStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Статус не найден")
    if status.equipments:
        raise HTTPException(status_code=400,
                            detail="Нельзя удалить статус,"
                            "к которому привязано оборудование")
    db.delete(status)
    db.commit()
