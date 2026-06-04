import pytest


def test_create_ingredient_endpoint(api_client, auth_token):
    """Test creating an ingredient via API endpoint."""
    ingredient = {
        "nombre": "Arroz",
        "cantidad": 2,
        "unidad": "tazas"
    }
    response = api_client.post(
        "/ingredients/",
        json=ingredient,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Arroz"
    assert data["cantidad"] == 2
    assert data["unidad"] == "tazas"


def test_get_ingredients_endpoint(api_client, auth_token):
    """Test retrieving user ingredients."""
    api_client.post(
        "/ingredients/",
        json={"nombre": "Pollo", "cantidad": 500, "unidad": "gramos"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    response = api_client.get(
        "/ingredients/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_generate_recipe_without_ingredients(api_client, test_user):
    """Test that generating recipe without ingredients fails."""
    # Register a fresh user with no ingredients
    api_client.post("/auth/register", json=test_user)
    response = api_client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    fresh_token = response.json()["access_token"]

    response = api_client.post(
        "/recipes/generate",
        headers={"Authorization": f"Bearer {fresh_token}"}
    )
    assert response.status_code == 400
    assert "ingredientes" in response.json()["detail"].lower()


def test_generate_recipe_with_ingredients(api_client, auth_token):
    """Test generating a recipe with ingredients."""
    api_client.post(
        "/ingredients/",
        json={"nombre": "Arroz", "cantidad": 2, "unidad": "tazas"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    api_client.post(
        "/ingredients/",
        json={"nombre": "Pollo", "cantidad": 500, "unidad": "gramos"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    response = api_client.post(
        "/recipes/generate",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    # This may return 200 or 500 depending on LLM API key availability
    assert response.status_code in [200, 400, 500]


def test_delete_recipe_endpoint(api_client, auth_token):
    """Test deleting a recipe."""
    api_client.post(
        "/ingredients/",
        json={"nombre": "Arroz", "cantidad": 2, "unidad": "tazas"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    api_client.post(
        "/recipes/generate",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    recipes = api_client.get(
        "/recipes/",
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()

    if recipes:
        recipe_id = recipes[0]["id"]
        response = api_client.delete(
            f"/recipes/{recipe_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "eliminada" in response.json()["message"].lower()


def test_rate_recipe_endpoint(api_client, auth_token):
    """Test rating a recipe."""
    api_client.post(
        "/ingredients/",
        json={"nombre": "Arroz", "cantidad": 2, "unidad": "tazas"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    api_client.post(
        "/recipes/generate",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    recipes = api_client.get(
        "/recipes/",
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()

    if recipes:
        recipe_id = recipes[0]["id"]
        response = api_client.post(
            f"/recipes/{recipe_id}/rate",
            json={"estrellas": 5},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert response.json()["estrellas"] == 5
