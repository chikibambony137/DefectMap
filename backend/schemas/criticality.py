from pydantic import BaseModel, ConfigDict


class CriticalityBase(BaseModel):
    """Базовые поля критичности"""
    name: str
    weight: int


class CriticalityCreate(CriticalityBase):
    """Создание критичности"""
    pass


class CriticalityResponse(CriticalityBase):
    """Ответ с критичностью"""
    id: int
    model_config = ConfigDict(from_attributes=True)