import json
import redis
from core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get(key: str):
    try:
        cached = redis_client.get(key)
        if cached:
            print("DATA FROM REDIS")
            return json.loads(cached)
    except redis.RedisError as e:
        print(f"Redis error in get: {e}")
    return None


def setex(key: str, ttl: int, data):
    try:
        redis_client.setex(key, ttl, json.dumps(data))
    except redis.RedisError as e:
        print(f"Redis error in setex: {e}")
    return data


def get_or_set(key: str, ttl: int, compute_func):
    """Получить из кэша, если нет — вычислить и сохранить"""
    cached = get(key)
    if cached is not None:
        return cached

    data = compute_func()
    setex(key, ttl, data)
    return data


def delete(key: str):
    """Удалить ключ из кэша"""
    try:
        redis_client.delete(key)
    except redis.RedisError as e:
        print(f"Redis error in delete: {e}")


def delete_pattern(pattern: str):
    """Удалить все ключи по шаблону (например, 'users:list:*')"""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except redis.RedisError as e:
        print(f"Redis error in delete_pattern: {e}")
