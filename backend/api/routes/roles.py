from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_admin_user
from models.role import Role
from models.user import User
from schemas.role import RoleCreate, RoleResponse

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=List[RoleResponse])
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Получить список ролей"""
    return db.query(Role).all()


@router.post("/", response_model=RoleResponse, status_code=201)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Создать роль"""
    existing = db.query(Role).filter(Role.name == role_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Роль с таким именем уже существует")
    
    role = Role(name=role_data.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role