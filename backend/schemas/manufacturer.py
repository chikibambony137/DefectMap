from typing import Optional
from pydantic import BaseModel, ConfigDict


class ManufacturerBase(BaseModel):
    name: str
    phone: str
    email: str
    address: str


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class ManufacturerResponse(ManufacturerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
