from pydantic import BaseModel, Field, ConfigDict


class IngredientCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    cantidad: float = Field(gt=0)
    unidad: str = Field(min_length=1, max_length=50)


class IngredientUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    cantidad: float | None = Field(default=None, gt=0)
    unidad: str | None = Field(default=None, min_length=1, max_length=50)


class IngredientResponse(BaseModel):
    id: int
    nombre: str
    cantidad: float
    unidad: str

    model_config = ConfigDict(from_attributes=True)