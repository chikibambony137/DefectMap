from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base


class DefectCriticality(Base):
    __tablename__ = "defect_criticality"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)  # low, medium, high
    weight = Column(Integer, nullable=False)  # для сортировки

    # Связи
    defects = relationship("Defect", back_populates="criticality")
