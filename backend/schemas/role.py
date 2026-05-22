from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    """Базовые поля роли"""
    name: str


class RoleCreate(RoleBase):
    """Создание роли"""
    pass


class RoleResponse(RoleBase):
    """Ответ с ролью"""
    id: int
    model_config = ConfigDict(from_attributes=True)
