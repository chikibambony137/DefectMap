from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user, get_current_admin_user
from core.security import get_password_hash
from models.user import User
from models.role import Role
from schemas.user import UserCreate, UserUpdate, UserResponse

from core import redis_client

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Получить список пользователей (только админ)"""

    def fetch_users():
        print("----------DATA FROM DB-------------")
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    
    return redis_client.get_or_set(f"users:list:{skip}:{limit}", 60, fetch_users)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    # временно сделал, что может обычный пользователь, по-хорошему надо новый роут сделать, 
    # в котором каждый может менять только свои данные
):
    """Получить пользователя по ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Создать пользователя (только админ)"""
    # Проверяем уникальность логина
    existing = db.query(User).filter(User.login == user_data.login).first()
    if existing:
        raise HTTPException(status_code=400, detail="Логин уже существует")
    
    # Проверяем существование роли
    role = db.query(Role).filter(Role.id == user_data.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Роль не найдена")
    
    new_user = User(
        surname=user_data.surname,
        name=user_data.name,
        middlename=user_data.middlename,
        login=user_data.login,
        hashed_password=get_password_hash(user_data.password),
        role_id=user_data.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
    # временно сделал, что может менять обычный пользователь, по-хорошему надо новый роут сделать, 
    # в котором каждый может менять только свои данные
):
    """Обновить пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Удалить пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")
    
    db.delete(user)
    db.commit()
    return user