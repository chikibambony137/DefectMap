from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base


class EquipmentStatus(Base):
    """Модель статуса прибора"""
    __tablename__ = "equipment_status"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(100), nullable=False)

    # Связи
    equipments = relationship("Equipment", back_populates="status")

    def __repr__(self):
        return f"<User {self.login}>"
