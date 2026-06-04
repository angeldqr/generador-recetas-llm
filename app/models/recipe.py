from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Recipe(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)

    nombre_plato = Column(String(150), nullable=False)
    ingredientes_json = Column(JSON, nullable=False)
    pasos_json = Column(JSON, nullable=False)
    tiempo_estimado = Column(String(100), nullable=False)
    dificultad = Column(String(50), nullable=False)

    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("User", back_populates="recetas")
    calificaciones = relationship("Rating", back_populates="receta")