import pytest
from pydantic import ValidationError

from app.schemas.ingredient import IngredientCreate


def test_ingredient_requires_positive_quantity():
    with pytest.raises(ValidationError):
        IngredientCreate(nombre="Arroz", cantidad=0, unidad="taza")


def test_ingredient_accepts_valid_payload():
    ingredient = IngredientCreate(nombre="Arroz", cantidad=2, unidad="tazas")

    assert ingredient.nombre == "Arroz"
    assert ingredient.cantidad == 2
    assert ingredient.unidad == "tazas"
