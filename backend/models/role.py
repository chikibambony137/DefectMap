from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base


class Role(Base):
    """Модель роли пользователя"""
    __tablename__ = "role"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(100), nullable=False)

    # Связи
    users = relationship("User", back_populates="role")
