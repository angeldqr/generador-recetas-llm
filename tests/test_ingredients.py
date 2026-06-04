import pytest
from app.schemas.ingredient import IngredientCreate, IngredientUpdate


def test_ingredient_create_valid():
    """Test that valid ingredient data passes schema validation."""
    ingredient = IngredientCreate(
        nombre="Pollo",
        cantidad=500,
        unidad="gramos"
    )
    assert ingredient.nombre == "Pollo"
    assert ingredient.cantidad == 500
    assert ingredient.unidad == "gramos"


def test_ingredient_create_short_name():
    """Test that ingredient name too short fails validation."""
    with pytest.raises(ValueError):
        IngredientCreate(nombre="A", cantidad=1, unidad="unidad")


def test_ingredient_create_negative_quantity():
    """Test that negative quantity fails validation."""
    with pytest.raises(ValueError):
        IngredientCreate(nombre="Arroz", cantidad=-5, unidad="tazas")


def test_ingredient_create_zero_quantity():
    """Test that zero quantity fails validation."""
    with pytest.raises(ValueError):
        IngredientCreate(nombre="Arroz", cantidad=0, unidad="tazas")


def test_ingredient_create_empty_unit():
    """Test that empty unit fails validation."""
    with pytest.raises(ValueError):
        IngredientCreate(nombre="Arroz", cantidad=1, unidad="")


def test_ingredient_update_partial():
    """Test that partial update works."""
    update = IngredientUpdate(cantidad=2.5)
    assert update.cantidad == 2.5
    assert update.nombre is None
    assert update.unidad is None
