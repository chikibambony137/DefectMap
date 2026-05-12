from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
    CookieTransport
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session

from core.config import settings
from core.database import SessionLocal
from models.user import User


# Транспорт для JWT (можно использовать Bearer или Cookie)
# BearerTransport - для Authorization: Bearer <token>
bearer_transport = BearerTransport(tokenUrl="auth/login")

# CookieTransport - для хранения токена в куки
cookie_transport = CookieTransport(
    cookie_name="optimetrik_auth",
    cookie_max_age=3600,
    cookie_secure=False,  # True в продакшене с HTTPS
    cookie_httponly=True,
    cookie_samesite="lax"
)


# Стратегия JWT
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=3600,  # 1 час
        token_audience=["fastapi-users:auth"],  # для совместимости
        algorithm=settings.ALGORITHM
    )


# Бэкенд аутентификации (выбери один или используй оба)
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,  # или bearer_transport
    get_strategy=get_jwt_strategy,
)


# База данных пользователей (синхронная версия)
class UserDatabase(SQLAlchemyUserDatabase):
    def __init__(self, session: Session):
        super().__init__(session, User)


# Функция для получения сессии БД
def get_user_db():
    db = SessionLocal()
    try:
        yield UserDatabase(db)
    finally:
        db.close()


# Менеджер пользователей
class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} ({user.email}) has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} forgot password. Token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Token: {token}")


# Функция для получения менеджера пользователей
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# FastAPI Users
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Текущий пользователь (dependency)
current_user = fastapi_users.current_user(active=True)
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user_optional = fastapi_users.current_user(optional=True)
