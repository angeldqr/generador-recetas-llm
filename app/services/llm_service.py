import json
import requests

from app.config import settings


def build_recipe_prompt(ingredientes) -> str:
    inventario = [
        {
            "nombre": ingrediente.nombre,
            "cantidad": ingrediente.cantidad,
            "unidad": ingrediente.unidad
        }
        for ingrediente in ingredientes
    ]

    return f"""
Eres un asistente culinario.

Con base en este inventario de ingredientes:

{json.dumps(inventario, ensure_ascii=False)}

Genera una receta posible usando principalmente esos ingredientes.

Devuelve únicamente un JSON válido con esta estructura:

{{
  "nombre_plato": "Nombre del plato",
  "ingredientes": [
    {{
      "nombre": "ingrediente",
      "cantidad": "cantidad necesaria"
    }}
  ],
  "pasos": [
    "Paso 1",
    "Paso 2"
  ],
  "tiempo_estimado": "30 minutos",
  "dificultad": "Fácil"
}}

No agregues texto fuera del JSON.
"""


def clean_json_response(content: str) -> dict:
    content = content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    data = json.loads(content)

    required_fields = [
        "nombre_plato",
        "ingredientes",
        "pasos",
        "tiempo_estimado",
        "dificultad"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Falta el campo requerido: {field}")

    return data


def generate_recipe_from_inventory(ingredientes) -> dict:
    prompt = build_recipe_prompt(ingredientes)

    if not settings.openrouter_api_key:
        return {
            "nombre_plato": "Receta de prueba",
            "ingredientes": [
                {
                    "nombre": ingrediente.nombre,
                    "cantidad": f"{ingrediente.cantidad} {ingrediente.unidad}"
                }
                for ingrediente in ingredientes
            ],
            "pasos": [
                "Lavar y preparar los ingredientes.",
                "Cocinar los ingredientes principales.",
                "Servir caliente."
            ],
            "tiempo_estimado": "30 minutos",
            "dificultad": "Fácil"
        }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": settings.openrouter_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Responde únicamente con JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        },
        timeout=60
    )

    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    return clean_json_response(content)