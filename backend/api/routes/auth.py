from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt

from api.dependencies import get_current_user, get_db
from core.config import settings
from core.security import get_password_hash, verify_password
from models.user import User
from models.role import Role
from schemas.auth import LoginResponse
from schemas.user import UserRegister, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя
    """
    # Проверка уникальности логина
    existing_login = db.query(User).filter(
        User.login == user_data.login).first()
    if existing_login:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует"
        )

    # роль по дефолту - наблюдатель (viewer). Другую роль назначает админ
    role = db.query(Role).filter(Role.name == "viewer").first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Роль не существует"
        )

    # Создаем нового пользователя
    db_user = User(
        surname=user_data.surname,
        name=user_data.name,
        middlename=user_data.middlename,
        login=user_data.login,
        hashed_password=get_password_hash(user_data.password),
        role=role,  # ← передаём объект Role, не ID!
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Логин пользователя, возвращает JWT токен
    """
    # Ищем пользователя по логину
    user = db.query(User).filter(
        User.login == form_data.username).first()

    if not user or not verify_password(form_data.password,
                                       user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаём JWT токен
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {
            "sub": str(user.id),
            "exp": datetime.now(timezone.utc) + access_token_expires
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "login": user.login,
        "role": user.role.name
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Получить информацию о текущем пользователе
    """
    return current_user
