from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    ingredientes = relationship("Ingredient", back_populates="usuario")
    recetas = relationship("Recipe", back_populates="usuario")
    calificaciones = relationship("Rating", back_populates="usuario")