from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Rating(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)
    estrellas = Column(Integer, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)

    usuario = relationship("User", back_populates="calificaciones")
    receta = relationship("Recipe", back_populates="calificaciones")