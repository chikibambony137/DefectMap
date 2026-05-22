from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base


class DefectStatus(Base):
    """Модель статуса дефекта"""
    __tablename__ = "defect_status"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(100), nullable=False)

    # Связи
    defects = relationship("Defect", back_populates="status")

    def __repr__(self):
        return f"<Status {self.name}>"
