from typing import Optional
from pydantic import BaseModel, ConfigDict


class DefectTypeBase(BaseModel):
    """Базовые поля типа дефекта"""
    name: str
    description: Optional[str] = None


class DefectTypeCreate(DefectTypeBase):
    """Создание типа дефекта"""
    pass


class DefectTypeUpdate(BaseModel):
    """Обновление типа дефекта"""
    name: Optional[str] = None
    description: Optional[str] = None


class DefectTypeResponse(DefectTypeBase):
    """Ответ с типом дефекта"""
    id: int
    model_config = ConfigDict(from_attributes=True)
