from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core import redis_client

from api.dependencies import (get_current_admin_user,
                              get_db,
                              get_current_user,
                              get_current_engineer_user)
from models.defect import Defect
from models.equipment import Equipment
from models.user import User
from schemas.defect import (
    DefectCreate, DefectUpdate, DefectResponse,
    DefectWithRelations, DefectGeoResponse
)

router = APIRouter(prefix="/defects", tags=["defects"])


@router.get("/", response_model=List[DefectResponse])
def get_defects(
    skip: int = 0,
    limit: int = 100,
    status_id: Optional[int] = Query(None),
    criticality_id: Optional[int] = Query(None),
    equipment_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить список дефектов с фильтрацией"""

    def fetch_defects():
        print("----------DATA FROM DB-------------")
        query = db.query(Defect)
        if status_id:
            query = query.filter(Defect.status_id == status_id)
        if criticality_id:
            query = query.filter(Defect.criticality_id == criticality_id)
        if equipment_id:
            query = query.filter(Defect.equipment_id == equipment_id)
        return query.order_by(
            Defect.created_at.desc()).offset(skip).limit(limit).all()

    #
    cache_key = f"defects:list:{skip}:{limit}:{status_id}:{criticality_id}:{equipment_id}" # noqa
    return redis_client.get_or_set(cache_key, 60, fetch_defects)


@router.get("/geo", response_model=List[DefectGeoResponse])
def get_defects_for_map(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Дефекты с координатами для карты"""

    def fetch_defects_for_map():
        print("----------DATA FROM DB-------------")
        defects = db.query(Defect).join(Defect.equipment).filter(
            Equipment.latitude.isnot(None),
            Equipment.longitude.isnot(None)
        ).all()
        return [
            {
                "id": d.id,
                "title": d.title,
                "criticality": d.criticality.name,
                "status": d.status.name,
                "status_id": d.status_id,
                "latitude": d.equipment.latitude,
                "longitude": d.equipment.longitude,
                "equipment_serial": d.equipment.serial_number,
                "equipment_model": d.equipment.model,
                "description": d.description,
                "created_at": d.created_at
            }
            for d in defects
        ]

    return redis_client.get_or_set("defects:geo:list",
                                   60, fetch_defects_for_map)


@router.get("/{defect_id}", response_model=DefectWithRelations)
def get_defect_by_id(
    defect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить дефект по ID со всеми связями"""

    def fetch_defect():
        print("----------DATA FROM DB-------------")
        defect = db.query(Defect).filter(Defect.id == defect_id).first()
        if not defect:
            raise HTTPException(status_code=404, detail="Дефект не найден")
        return {
            **defect.__dict__,
            "criticality_name": defect.criticality.name,
            "criticality_weight": defect.criticality.weight,
            "defect_type_name": defect.defect_type.name,
            "status_name": defect.status.name,
            "equipment_serial": defect.equipment.serial_number,
            "equipment_model": defect.equipment.model,
            "user_surname": defect.user.surname,
            "user_name": defect.user.name,
            "user_login": defect.user.login
        }

    return redis_client.get_or_set(f"defects:{defect_id}", 60, fetch_defect)


@router.post("/", response_model=DefectResponse, status_code=201)
def create_defect(
    defect_data: DefectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_engineer_user)
):
    """Создать дефект"""
    equipment = db.query(Equipment).filter(
        Equipment.id == defect_data.equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=400, detail="Оборудование не найдено")

    defect = Defect(
        **defect_data.model_dump(),
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(defect)
    db.commit()
    db.refresh(defect)

    redis_client.delete_pattern("defects:list:*")
    redis_client.delete("defects:geo:list")

    return defect


@router.put("/{defect_id}", response_model=DefectResponse)
def update_defect(
    defect_id: int,
    defect_data: DefectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_engineer_user)
):
    """Обновить дефект"""
    defect = db.query(Defect).filter(Defect.id == defect_id).first()
    if not defect:
        raise HTTPException(status_code=404, detail="Дефект не найден")

    update_data = defect_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(defect, field, value)

    db.commit()
    db.refresh(defect)

    redis_client.delete(f"defects:{defect_id}")
    redis_client.delete_pattern("defects:list:*")
    redis_client.delete("defects:geo:list")

    return defect


@router.delete("/{defect_id}", status_code=204)
def delete_defect(
    defect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Удалить дефект (только админ)"""
    defect = db.query(Defect).filter(Defect.id == defect_id).first()
    if not defect:
        raise HTTPException(status_code=404, detail="Дефект не найден")

    db.delete(defect)
    db.commit()

    redis_client.delete(f"defects:{defect_id}")
    redis_client.delete_pattern("defects:list:*")
    redis_client.delete("defects:geo:list")
