import json
import re
import requests

from app.config import settings


def build_recipe_prompt(ingredientes) -> str:
    """
    Construye un prompt estricto que fuerza al LLM a usar EXCLUSIVAMENTE
    los ingredientes del inventario del usuario. No permite ingredientes adicionales.
    """
    inventario = [
        {
            "nombre": ingrediente.nombre,
            "cantidad": ingrediente.cantidad,
            "unidad": ingrediente.unidad
        }
        for ingrediente in ingredientes
    ]

    nombres_ingredientes = [i["nombre"] for i in inventario]

    return f"""
Eres un chef experto y creativo. Tu tarea es generar una receta usando EXCLUSIVA Y UNICAMENTE los ingredientes que te proporciono a continuacion.

REGLAS ESTRICTAS:
1. Usa SOLO los ingredientes de la lista. NO agregues ningun ingrediente adicional.
2. NO incluyas ingredientes basicos implicitos como "sal", "pimienta", "aceite", "agua" o "ajo" a menos que esten explicitamente en la lista.
3. Si no puedes crear una receta real con los ingredientes proporcionados, devuelve exactamente: {{"error": "No es posible crear una receta con los ingredientes disponibles"}}
4. Las cantidades de los ingredientes en la receta deben respetar las cantidades disponibles en el inventario (no pedir mas de lo que hay).
5. Devuelve UNICAMENTE un JSON valido. Nada de texto adicional.

Inventario de ingredientes del usuario:

{json.dumps(inventario, ensure_ascii=False, indent=2)}

Formato JSON requerido:
{{
  "nombre_plato": "Nombre del plato",
  "ingredientes": [
    {{
      "nombre": "nombre exacto del ingrediente (debe estar en el inventario)",
      "cantidad": "cantidad a usar"
    }}
  ],
  "pasos": [
    "Paso 1...",
    "Paso 2..."
  ],
  "tiempo_estimado": "30 minutos",
  "dificultad": "Facil|Media|Dificil"
}}

Valida que cada ingrediente en "ingredientes" esté en esta lista: {', '.join(nombres_ingredientes)}.
"""


def clean_json_response(content: str | None) -> dict:
    """Limpia la respuesta del LLM y la parsea como JSON."""
    if content is None:
        raise ValueError("El LLM devolvio una respuesta vacia (None)")

    content = content.strip()

    if not content:
        raise ValueError("El LLM devolvio una respuesta vacia")

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"La respuesta del LLM no es un JSON valido: {str(e)}")

    if "error" in data:
        return data

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


def validate_recipe_ingredients(recipe_data: dict, user_ingredients: list) -> dict:
    """
    Valida que todos los ingredientes de la receta esten en el inventario del usuario.
    Si encuentra ingredientes extras, lanza ValueError.
    """
    if "error" in recipe_data:
        return recipe_data

    if not user_ingredients:
        return recipe_data

    # Handle both dict-like objects and attribute-based objects (like MockIngredient)
    first = user_ingredients[0]
    if hasattr(first, "nombre"):
        user_names = {i.nombre.lower().strip() for i in user_ingredients}
    else:
        user_names = {i["nombre"].lower().strip() for i in user_ingredients}

    recipe_ingredients = recipe_data.get("ingredientes", [])
    extras = []

    for ing in recipe_ingredients:
        nombre = ing.get("nombre", "").lower().strip()
        if nombre and nombre not in user_names:
            extras.append(ing.get("nombre", nombre))

    if extras:
        raise ValueError(
            f"La receta contiene ingredientes no disponibles en el inventario: {', '.join(extras)}. "
            f"Solo se permiten: {', '.join(sorted(user_names))}."
        )

    return recipe_data


def generate_recipe_from_inventory(ingredientes) -> dict:
    """Genera una receta usando el LLM con validacion estricta de inventario."""
    prompt = build_recipe_prompt(ingredientes)

    if not settings.openrouter_api_key:
        # Fallback: receta de prueba usando solo los ingredientes del usuario
        return {
            "nombre_plato": "Plato de prueba",
            "ingredientes": [
                {
                    "nombre": ingrediente.nombre,
                    "cantidad": f"{ingrediente.cantidad} {ingrediente.unidad}"
                }
                for ingrediente in ingredientes
            ],
            "pasos": [
                "Preparar los ingredientes del inventario.",
                "Cocinar usando solo los ingredientes disponibles.",
                "Servir y disfrutar."
            ],
            "tiempo_estimado": "30 minutos",
            "dificultad": "Facil"
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
                    "content": "Responde unicamente con JSON valido. No agregues texto ni markdown fuera del JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.5,
            "max_tokens": 800
        },
        timeout=60
    )

    response.raise_for_status()

    response_data = response.json()
    choices = response_data.get("choices", [])
    
    if not choices:
        raise ValueError("El LLM no devolvio ninguna respuesta (choices vacio)")
    
    message = choices[0].get("message", {})
    content = message.get("content")
    
    if content is None:
        raise ValueError("El LLM devolvio message.content = None")
    
    recipe_data = clean_json_response(content)

    # Validacion estricta: solo ingredientes del inventario
    validate_recipe_ingredients(recipe_data, ingredientes)

    return recipe_data
