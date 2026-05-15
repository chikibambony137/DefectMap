from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db
from api.routes import (
    auth_router, users_router, roles_router,
    equipment_router, equipment_statuses_router, defects_router,
    defect_types_router, defect_statuses_router, criticalities_router,
    manufacturers_router
)

app = FastAPI(title="DefectMap API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(equipment_router)
app.include_router(equipment_statuses_router)
app.include_router(defects_router)
app.include_router(defect_types_router)
app.include_router(defect_statuses_router)
app.include_router(criticalities_router)
app.include_router(manufacturers_router)


@app.get("/")
def health_check(db: Session = Depends(get_db)):
    """
    Проверка работоспособности API и подключения к БД
    """
    try:
        # Пробуем выполнить запрос к БД
        db.execute(text("SELECT 1")).scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "✅ API и БД работают"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
