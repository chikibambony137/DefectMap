from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DefectBase(BaseModel):
    title: str
    description: Optional[str] = None
    status_id: int = 3          # 3 = "Открыт" по данным из БД
    photo_url: Optional[str] = None
    criticality_id: int
    equipment_id: int
    defect_type_id: int


class DefectCreate(DefectBase):
    pass


class DefectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    photo_url: Optional[str] = None
    resolved_at: Optional[datetime] = None
    criticality_id: Optional[int] = None
    defect_type_id: Optional[int] = None
    equipment_id: Optional[int] = None


class DefectResponse(DefectBase):
    id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class DefectWithRelations(DefectResponse):
    criticality_name: str
    criticality_weight: int
    defect_type_name: str
    status_name: str
    equipment_serial: str
    equipment_model: str
    user_surname: str
    user_name: str
    user_login: str


class DefectGeoResponse(BaseModel):
    id: int
    title: str
    criticality: str
    status: str                 # человекочитаемое имя статуса
    status_id: int
    latitude: float
    longitude: float
    equipment_serial: str
    equipment_model: str
    description: Optional[str] = None
    created_at: datetime
