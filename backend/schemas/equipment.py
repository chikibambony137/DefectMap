from typing import Optional
from datetime import date
from pydantic import BaseModel, ConfigDict


class EquipmentBase(BaseModel):
    serial_number: str
    model: str
    manufacturer_id: int
    location_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    installation_date: Optional[date] = None
    status_id: int


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    serial_number: Optional[str] = None
    model: Optional[str] = None
    manufacturer_id: Optional[int] = None
    location_address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    installation_date: Optional[date] = None
    status_id: Optional[int] = None


class EquipmentResponse(EquipmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EquipmentWithStats(EquipmentResponse):
    defects_count: int
    open_defects_count: int
