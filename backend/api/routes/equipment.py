from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.dependencies import (get_current_admin_user,
                              get_db, get_current_user,
                              get_current_engineer_user)
from models.equipment import Equipment
from models.defect import Defect
from models.defect_status import DefectStatus
from models.user import User
from schemas.equipment import (
    EquipmentCreate, EquipmentUpdate,
    EquipmentResponse, EquipmentWithStats
)
from core import redis_client

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("/", response_model=List[EquipmentResponse])
def get_equipment(
    skip: int = 0,
    limit: int = 100,
    status_id: Optional[int] = Query(None),
    manufacturer_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить список оборудования"""

    def fetch_equipment():
        print("--------------DATA FROM DB---------------")
        query = db.query(Equipment)
        if status_id:
            query = query.filter(Equipment.status_id == status_id)
        if manufacturer_id:
            query = query.filter(
                Equipment.manufacturer_id == manufacturer_id)
        return query.offset(skip).limit(limit).all()

    cache_key = f"equipment:list:{skip}:{limit}:{status_id}:{manufacturer_id}" # noqa
    return redis_client.get_or_set(cache_key, 60, fetch_equipment)


@router.get("/with-stats", response_model=List[EquipmentWithStats])
def get_equipment_with_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Оборудование со статистикой дефектов"""

    def fetch_equipment_with_stats():
        print("--------------DATA FROM DB---------------")
        open_status = db.query(DefectStatus).filter(
            DefectStatus.name == "Открыт").first()
        open_status_id = open_status.id if open_status else None

        equipment_list = db.query(Equipment).all()
        result = []
        for eq in equipment_list:
            defects_count = db.query(Defect).filter(
                Defect.equipment_id == eq.id).count()
            open_defects = db.query(Defect).filter(
                Defect.equipment_id == eq.id,
                Defect.status_id == open_status_id
            ).count() if open_status_id else 0

            result.append({
                "id": eq.id,
                "serial_number": eq.serial_number,
                "model": eq.model,
                "manufacturer_id": eq.manufacturer_id,
                "location_address": eq.location_address,
                "latitude": eq.latitude,
                "longitude": eq.longitude,
                "installation_date": eq.installation_date,
                "status_id": eq.status_id,
                "defects_count": defects_count,
                "open_defects_count": open_defects
            })
            
        return result

    return redis_client.get_or_set("equipment:with-stats",
                                   60, fetch_equipment_with_stats)


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment_by_id(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить оборудование по ID"""

    def fetch_equipment():
        print("--------------DATA FROM DB---------------")
        equipment = db.query(Equipment).filter(
            Equipment.id == equipment_id).first()
        if not equipment:
            raise HTTPException(status_code=404,
                                detail="Оборудование не найдено")
        return equipment

    return redis_client.get_or_set(f"equipment:{equipment_id}", 60, fetch_equipment) # noqa


@router.post("/", response_model=EquipmentResponse, status_code=201)
def create_equipment(
    equipment_data: EquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_engineer_user)
):
    """Создать оборудование"""
    existing = db.query(Equipment).filter(
        Equipment.serial_number == equipment_data.serial_number
    ).first()
    if existing:
        raise HTTPException(status_code=400,
                            detail="Прибор с таким серийным"
                            "номером уже существует")

    equipment = Equipment(**equipment_data.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)

    redis_client.delete_pattern("equipment:list:*")
    redis_client.delete("equipment:with-stats")

    return equipment


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    equipment_data: EquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_engineer_user)
):
    """Обновить оборудование"""
    equipment = db.query(Equipment).filter(
        Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Оборудование не найдено")

    update_data = equipment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(equipment, field, value)

    db.commit()
    db.refresh(equipment)

    redis_client.delete(f"equipment:{equipment_id}")
    redis_client.delete_pattern("equipment:list:*")
    redis_client.delete("equipment:with-stats")

    return equipment


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Удалить оборудование (только админ)"""
    equipment = db.query(Equipment).filter(
        Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404,
                            detail="Оборудование не найдено")

    defects_count = db.query(Defect).filter(
        Defect.equipment_id == equipment_id).count()
    if defects_count > 0:
        raise HTTPException(status_code=400,
                            detail="Нельзя удалить прибор с дефектами")

    db.delete(equipment)
    db.commit()

    redis_client.delete(f"equipment:{equipment_id}")
    redis_client.delete_pattern("equipment:list:*")
    redis_client.delete("equipment:with-stats")
