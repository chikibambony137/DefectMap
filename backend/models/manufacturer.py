from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base


class Manufacturer(Base):
    """Модель производителя"""
    __tablename__ = "manufacturer"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(200), nullable=False)
    phone = Column("phone", String(13), nullable=False)
    email = Column("email", String(100), nullable=False)
    address = Column("address", String(200), nullable=False)

    # Связи
    equipments = relationship("Equipment", back_populates="manufacturer")

    def __repr__(self):
        return f"<Manufacturer {self.name}>"
