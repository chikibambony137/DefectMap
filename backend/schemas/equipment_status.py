from pydantic import BaseModel, ConfigDict


class EquipmentStatusBase(BaseModel):
    name: str


class EquipmentStatusCreate(EquipmentStatusBase):
    pass


class EquipmentStatusResponse(EquipmentStatusBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
