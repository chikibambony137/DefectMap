from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user, get_current_admin_user, get_current_engineer_user
from models.manufacturer import Manufacturer
from schemas.manufacturer import ManufacturerCreate, ManufacturerUpdate, ManufacturerResponse

router = APIRouter(prefix="/manufacturers", tags=["manufacturers"])


@router.get("/", response_model=List[ManufacturerResponse])
def get_manufacturers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Manufacturer).all()


@router.get("/{manufacturer_id}", response_model=ManufacturerResponse)
def get_manufacturer_by_id(
    manufacturer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Производитель не найден")
    return manufacturer


@router.post("/", response_model=ManufacturerResponse, status_code=201)
def create_manufacturer(
    data: ManufacturerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_engineer_user)
):
    manufacturer = Manufacturer(**data.model_dump())
    db.add(manufacturer)
    db.commit()
    db.refresh(manufacturer)
    return manufacturer


@router.put("/{manufacturer_id}", response_model=ManufacturerResponse)
def update_manufacturer(
    manufacturer_id: int,
    data: ManufacturerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_engineer_user)
):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Производитель не найден")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(manufacturer, field, value)

    db.commit()
    db.refresh(manufacturer)
    return manufacturer


@router.delete("/{manufacturer_id}", status_code=204)
def delete_manufacturer(
    manufacturer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Производитель не найден")
    if manufacturer.equipments:
        raise HTTPException(status_code=400, detail="Нельзя удалить производителя, за которым закреплено оборудование")
    db.delete(manufacturer)
    db.commit()