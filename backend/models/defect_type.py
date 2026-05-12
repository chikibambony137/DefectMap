from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base

class DefectType(Base):
    """Тип дефекта (справочник)"""
    __tablename__ = "defect_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=True)

    # Связи
    defects = relationship("Defect", back_populates="defect_type")

    def __repr__(self):
        return f"<DefectType {self.name}>"