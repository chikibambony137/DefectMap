from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True, index=True)
    surname = Column("surname", String(100), nullable=False)
    name = Column("name", String(100), nullable=False)
    middlename = Column("middlename", String(100), nullable=True)
    login = Column("login", String(100), nullable=False, unique=True)
    hashed_password = Column("hashed_password", String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

    # Связи
    role = relationship("Role", back_populates="users")
    defects = relationship("Defect", back_populates="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.login}>"
