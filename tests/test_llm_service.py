from types import SimpleNamespace

import pytest

from app.services import llm_service


def make_ingredient(nombre="Arroz", cantidad=2, unidad="tazas"):
    return SimpleNamespace(nombre=nombre, cantidad=cantidad, unidad=unidad)


def test_build_recipe_prompt_includes_inventory_items():
    prompt = llm_service.build_recipe_prompt([
        make_ingredient("Arroz", 2, "tazas"),
        make_ingredient("Tomate", 3, "unidades"),
    ])

    assert "Arroz" in prompt
    assert "Tomate" in prompt
    assert "nombre_plato" in prompt
    assert "No agregues texto fuera del JSON" in prompt


def test_clean_json_response_parses_fenced_json():
    parsed = llm_service.clean_json_response(
        """```json
        {
          "nombre_plato": "Arroz con tomate",
          "ingredientes": [{"nombre": "Arroz", "cantidad": "2 tazas"}],
          "pasos": ["Cocinar"],
          "tiempo_estimado": "20 minutos",
          "dificultad": "Fácil"
        }
        ```"""
    )

    assert parsed["nombre_plato"] == "Arroz con tomate"
    assert parsed["dificultad"] == "Fácil"


def test_clean_json_response_rejects_missing_fields():
    with pytest.raises(ValueError):
        llm_service.clean_json_response('{"nombre_plato": "Incompleta"}')


def test_generate_recipe_uses_fallback_without_api_key(monkeypatch):
    monkeypatch.setattr(llm_service.settings, "openrouter_api_key", None)

    recipe = llm_service.generate_recipe_from_inventory([
        make_ingredient("Papa", 4, "unidades")
    ])

    assert recipe["nombre_plato"] == "Receta de prueba"
    assert recipe["ingredientes"][0]["nombre"] == "Papa"
