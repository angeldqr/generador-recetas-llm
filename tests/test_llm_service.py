import pytest
from app.services.llm_service import build_recipe_prompt, clean_json_response, validate_recipe_ingredients


def test_build_recipe_prompt_strict():
    """Test that the prompt includes strict instructions and all user ingredients."""
    class MockIngredient:
        def __init__(self, nombre, cantidad, unidad):
            self.nombre = nombre
            self.cantidad = cantidad
            self.unidad = unidad

    ingredients = [
        MockIngredient("Arroz", 2, "tazas"),
        MockIngredient("Pollo", 500, "gramos"),
    ]

    prompt = build_recipe_prompt(ingredients)

    assert "EXCLUSIVA Y UNICAMENTE" in prompt
    assert "NO agregues ningun ingrediente adicional" in prompt
    assert "Arroz" in prompt
    assert "Pollo" in prompt
    assert "2" in prompt
    assert "500" in prompt


def test_clean_json_response_valid():
    """Test parsing of valid JSON response."""
    json_str = '{"nombre_plato": "Arroz con pollo", "ingredientes": [{"nombre": "Arroz", "cantidad": "2 tazas"}], "pasos": ["Cocinar"], "tiempo_estimado": "30 min", "dificultad": "Facil"}'
    data = clean_json_response(json_str)
    assert data["nombre_plato"] == "Arroz con pollo"
    assert len(data["ingredientes"]) == 1


def test_clean_json_response_with_markdown():
    """Test parsing JSON wrapped in markdown code fences."""
    json_str = '```json\n{"nombre_plato": "Test", "ingredientes": [], "pasos": [], "tiempo_estimado": "10m", "dificultad": "Facil"}\n```'
    data = clean_json_response(json_str)
    assert data["nombre_plato"] == "Test"


def test_clean_json_response_missing_field():
    """Test that missing required fields raise ValueError."""
    json_str = '{"nombre_plato": "Test", "ingredientes": []}'
    with pytest.raises(ValueError):
        clean_json_response(json_str)


def test_validate_recipe_ingredients_valid():
    """Test that recipe with only user ingredients passes validation."""
    class MockIngredient:
        def __init__(self, nombre):
            self.nombre = nombre

    user_ingredients = [MockIngredient("Arroz"), MockIngredient("Pollo")]
    recipe_data = {
        "nombre_plato": "Arroz con pollo",
        "ingredientes": [
            {"nombre": "Arroz", "cantidad": "2 tazas"},
            {"nombre": "Pollo", "cantidad": "500g"}
        ],
        "pasos": ["Cocinar"],
        "tiempo_estimado": "30m",
        "dificultad": "Facil"
    }

    result = validate_recipe_ingredients(recipe_data, user_ingredients)
    assert result["nombre_plato"] == "Arroz con pollo"


def test_validate_recipe_ingredients_with_extra():
    """Test that recipe with extra ingredients raises ValueError."""
    class MockIngredient:
        def __init__(self, nombre):
            self.nombre = nombre

    user_ingredients = [MockIngredient("Arroz")]
    recipe_data = {
        "nombre_plato": "Arroz con pollo",
        "ingredientes": [
            {"nombre": "Arroz", "cantidad": "2 tazas"},
            {"nombre": "Pollo", "cantidad": "500g"},
            {"nombre": "Sal", "cantidad": "al gusto"}
        ],
        "pasos": ["Cocinar"],
        "tiempo_estimado": "30m",
        "dificultad": "Facil"
    }

    with pytest.raises(ValueError) as exc_info:
        validate_recipe_ingredients(recipe_data, user_ingredients)
    assert "ingredientes no disponibles" in str(exc_info.value)


def test_validate_recipe_ingredients_error_field():
    """Test that recipe with error field passes through without validation."""
    class MockIngredient:
        def __init__(self, nombre):
            self.nombre = nombre

    user_ingredients = [MockIngredient("Arroz")]
    recipe_data = {"error": "No es posible crear una receta con los ingredientes disponibles"}

    result = validate_recipe_ingredients(recipe_data, user_ingredients)
    assert "error" in result
