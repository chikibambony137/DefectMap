from pydantic_settings import BaseSettings
from pydantic import ConfigDict

import os
from dotenv import load_dotenv

# Загружаем .env файл (на всякий случай, но Docker уже передаст переменные)
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL",
                                  "postgresql://postgres:0053@localhost:5432/Diplom") # noqa

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Настройки приложения
    PROJECT_NAME: str = "DefectMap"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "API для учёта дефектов электротехнических приборов"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
