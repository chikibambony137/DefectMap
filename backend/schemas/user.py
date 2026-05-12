from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """Базовые поля пользователя"""
    surname: str
    name: str
    middlename: Optional[str] = None
    login: str
    role_id: int


class UserCreate(UserBase):
    """Создание пользователя"""
    password: str


class UserRegister(BaseModel):
    """Схема для регистрации нового пользователя"""
    surname: str
    name: str
    middlename: Optional[str] = None
    login: str
    password: str


class UserUpdate(BaseModel):
    """Обновление пользователя (все поля опциональны)"""
    surname: Optional[str] = None
    name: Optional[str] = None
    middlename: Optional[str] = None
    login: Optional[str] = None
    role_id: Optional[int] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """Пользователь из БД"""
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserInDB):
    """Ответ с пользователем (без пароля)"""
    pass


class UserWithRole(UserResponse):
    """Пользователь с данными роли"""
    role_name: str