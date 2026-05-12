from typing import Optional
from datetime import date
from pydantic import BaseModel, ConfigDict


class EquipmentBase(BaseModel):
    """Базовые поля оборудования"""
    serial_number: str
    model: str
    manufacturer: Optional[str] = None
    location_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    installation_date: Optional[date] = None
    status: str = "active"


class EquipmentCreate(EquipmentBase):
    """Создание оборудования"""
    pass


class EquipmentUpdate(BaseModel):
    """Обновление оборудования (все поля опциональны)"""
    serial_number: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    location_address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    installation_date: Optional[date] = None
    status: Optional[str] = None


class EquipmentResponse(EquipmentBase):
    """Ответ с оборудованием"""
    id: int
    model_config = ConfigDict(from_attributes=True)


class EquipmentWithStats(EquipmentResponse):
    """Оборудование со статистикой дефектов"""
    defects_count: int
    open_defects_count: int