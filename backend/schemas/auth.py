from pydantic import BaseModel


class Token(BaseModel):
    """JWT токен"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Данные в токене"""
    user_id: int


class LoginRequest(BaseModel):
    """Запрос на логин"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Ответ на логин"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    login: str
    role: str