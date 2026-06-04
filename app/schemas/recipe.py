from typing import Any
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class RecipeResponse(BaseModel):
    id: int
    nombre_plato: str
    ingredientes_json: list[dict[str, Any]]
    pasos_json: list[str]
    tiempo_estimado: str
    dificultad: str
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)


class RatingCreate(BaseModel):
    estrellas: int = Field(ge=1, le=5)