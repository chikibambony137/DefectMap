from sqlalchemy import String, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Defect(Base):
    """Модель дефекта прибора"""
    __tablename__ = "defect"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="open")  # open, in_progress, closed
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    photo_url = Column(String(500), nullable=True)

    # Внешние ключи
    criticality_id = Column(Integer, ForeignKey("defect_criticality.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    defect_type_id = Column(Integer, ForeignKey("defect_type.id"), nullable=False)

    # Связи — используем правильное имя класса DefectCriticality
    criticality = relationship("DefectCriticality", back_populates="defects")
    equipment = relationship("Equipment", back_populates="defects")
    user = relationship("User", back_populates="defects")
    defect_type = relationship("DefectType", back_populates="defects")

    def __repr__(self):
        return f"<Defect {self.title}>"