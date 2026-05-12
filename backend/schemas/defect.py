from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DefectBase(BaseModel):
    """Базовые поля дефекта"""
    title: str
    description: Optional[str] = None
    status: str = "open"
    photo_url: Optional[str] = None
    criticality_id: int
    equipment_id: int
    defect_type_id: int


class DefectCreate(DefectBase):
    """Создание дефекта"""
    pass


class DefectUpdate(BaseModel):
    """Обновление дефекта (все поля опциональны)"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    photo_url: Optional[str] = None
    resolved_at: Optional[datetime] = None
    criticality_id: Optional[int] = None
    defect_type_id: Optional[int] = None
    equipment_id: Optional[int] = None


class DefectResponse(DefectBase):
    """Ответ с дефектом"""
    id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class DefectWithRelations(DefectResponse):
    """Дефект со связанными данными"""
    criticality_name: str
    criticality_weight: int
    defect_type_name: str
    equipment_serial: str
    equipment_model: str
    user_surname: str
    user_name: str
    user_login: str


class DefectGeoResponse(BaseModel):
    """Дефект для карты (геоданные)"""
    id: int
    title: str
    criticality: str  # low, medium, high
    status: str
    latitude: float
    longitude: float
    equipment_serial: str
    equipment_model: str
    description: Optional[str] = None
    created_at: datetime