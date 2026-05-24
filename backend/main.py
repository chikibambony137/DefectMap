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

from fastapi import WebSocket, WebSocketDisconnect
from core.websocket_manager import manager
from contextlib import asynccontextmanager
import asyncio
import redis.asyncio as redis
import os

LOCAL_MODE = os.getenv("LOCAL_MODE", "false").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not LOCAL_MODE:
        task = asyncio.create_task(listen_to_redis())
        print("🚀 Redis listener task created")
    else:
        print("⚡ LOCAL_MODE: Redis listener skipped")
    yield
    if not LOCAL_MODE:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("Redis listener stopped")

app = FastAPI(title="DefectMap API", lifespan=lifespan)


async def listen_to_redis():
    print("🔄 Redis listener starting...")
    while True:
        try:
            r = redis.Redis.from_url(
                "redis://redis:6379/0",
                decode_responses=True
            )
            pubsub = r.pubsub()
            await pubsub.subscribe("defects")
            print("✅ Subscribed to Redis channel 'defects'")

            async for message in pubsub.listen():
                print(f"📨 Raw message: {message}")
                if message["type"] == "message":
                    print(f"📨 Broadcasting: {message['data']}")
                    await manager.broadcast(message["data"])

        except asyncio.CancelledError:
            print("Redis listener cancelled")
            break
        except Exception as e:
            print(f"❌ Redis listener error: {e}. Reconnecting in 3s...")
            await asyncio.sleep(3)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if LOCAL_MODE:
        await websocket.close(code=1001)  # 1001 = Going Away
        return
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


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
