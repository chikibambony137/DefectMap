import json
import redis
from datetime import date, datetime
from decimal import Decimal
from core.config import settings

try:
    _client = redis.Redis.from_url(settings.REDIS_URL,
                                   decode_responses=True,
                                   socket_connect_timeout=2)
    _client.ping()
    REDIS_AVAILABLE = True
    print("✅ Redis connected")
except Exception:
    _client = None
    REDIS_AVAILABLE = False
    print("⚠️  Redis unavailable, caching disabled")


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if hasattr(obj, "__dict__"):
            return {k: v for k, v in obj.__dict__.items()
                    if not k.startswith("_")}
        return super().default(obj)


def get(key: str):
    if not REDIS_AVAILABLE:
        return None
    try:
        cached = _client.get(key)
        if cached:
            print("DATA FROM REDIS")
            return json.loads(cached)
    except redis.RedisError as e:
        print(f"Redis error in get: {e}")
    return None


def setex(key: str, ttl: int, data):
    if not REDIS_AVAILABLE:
        return data
    try:
        _client.setex(key, ttl, json.dumps(data, cls=CustomEncoder))
    except redis.RedisError as e:
        print(f"Redis error in setex: {e}")
    return data


def get_or_set(key: str, ttl: int, compute_func):
    """Получить из кэша, если нет — вычислить и сохранить"""
    if not REDIS_AVAILABLE:
        return compute_func()

    cached = get(key)
    if cached is not None:
        return cached

    data = compute_func()
    setex(key, ttl, data)
    return data


def delete(key: str):
    """Удалить ключ из кэша"""
    if not REDIS_AVAILABLE:
        return
    try:
        _client.delete(key)
    except redis.RedisError as e:
        print(f"Redis error in delete: {e}")


def delete_pattern(pattern: str):
    """Удалить все ключи по шаблону (например, 'users:list:*')"""
    if not REDIS_AVAILABLE:
        return
    try:
        keys = _client.keys(pattern)
        if keys:
            _client.delete(*keys)
    except redis.RedisError as e:
        print(f"Redis error in delete_pattern: {e}")


# Websocket func
def publish(channel: str, event_type: str, data: dict):
    if not REDIS_AVAILABLE:
        return
    try:
        message = json.dumps({"event": event_type, "data": data})
        _client.publish(channel, message)
    except redis.RedisError as e:
        print(f"Redis error in publish: {e}")
