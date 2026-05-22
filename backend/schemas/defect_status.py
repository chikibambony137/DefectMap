from pydantic import BaseModel, ConfigDict


class DefectStatusBase(BaseModel):
    name: str


class DefectStatusCreate(DefectStatusBase):
    pass


class DefectStatusResponse(DefectStatusBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
