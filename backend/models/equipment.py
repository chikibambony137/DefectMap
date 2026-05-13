from sqlalchemy import ForeignKey, String, Column, Integer, Float, Date
from sqlalchemy.orm import relationship
from core.database import Base

class Equipment(Base):
    """Модель оборудования (электротехнические приборы)"""
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(100), nullable=False, unique=True)
    model = Column(String(200), nullable=False)
    location_address = Column(String(500), nullable=False)  # адрес установки
    latitude = Column(Float, nullable=True)   # широта (для карты)
    longitude = Column(Float, nullable=True)  # долгота (для карты)
    installation_date = Column(Date, nullable=True)
    
    # Внешние ключи
    manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("equipment_status.id"), nullable=False)

    # Связи
    manufacturer = relationship("Manufacturer", back_populates="equipments")
    equipment_status = relationship("EquipmentStatus", back_populates="equipments")
    defects = relationship("Defect", back_populates="equipment", lazy="dynamic")

    def __repr__(self):
        return f"<Equipment {self.serial_number} ({self.model})>"
