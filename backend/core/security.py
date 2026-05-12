import bcrypt
import logging

logger = logging.getLogger(__name__)


def get_password_hash(password: str) -> str:
    """
    Хеширование пароля с использованием bcrypt напрямую
    """
    logger.debug(f"Хеширование пароля: '{password}'")

    # Конвертируем в байты и обрезаем до 72 байт (ограничение bcrypt)
    password_bytes = password.encode('utf-8')[:72]

    # Генерируем соль и хеш
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    # Возвращаем как строку
    hashed_str = hashed_bytes.decode('utf-8')
    logger.debug(f"Хеш создан: {hashed_str[:20]}...")

    return hashed_str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля
    """
    logger.debug("Проверка пароля")

    # Конвертируем в байты
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')

    # Проверяем
    result = bcrypt.checkpw(password_bytes, hashed_bytes)
    logger.debug(f"Результат проверки: {result}")

    return result
