from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from core.database import SessionLocal
from core.config import settings
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_db() -> Generator:
    """
    Зависимость для получения сессии базы данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db),
                           token: str = Depends(oauth2_scheme)) -> User:
    """
    Получить текущего пользователя по JWT токену
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не предоставлен токен авторизации",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_admin_user(
        current_user: User = Depends(get_current_user)) -> User:
    """
    Проверка, что пользователь - администратор
    (по роли, а не по полю admin_role)
    """
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуются права администратора"
        )
    return current_user


async def get_current_engineer_user(
        current_user: User = Depends(get_current_user)) -> User:
    """
    Проверка, что пользователь - инженер или администратор
    """
    if current_user.role.name not in ["admin", "engineer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуются права инженера"
        )
    return current_user


async def get_current_user_optional(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)) -> Optional[User]:
    """
    Получить текущего пользователя или None, если не авторизован
    """
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None

        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except JWTError:
        return None
