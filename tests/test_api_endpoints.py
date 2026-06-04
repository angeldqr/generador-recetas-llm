def test_register_user_endpoint(client):
    response = client.post(
        "/auth/register",
        json={
            "nombre": "Ángel",
            "email": "angel@example.com",
            "password": "secret123",
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == "angel@example.com"


def test_protected_ingredients_endpoint_requires_token(client):
    response = client.get("/ingredients/")

    assert response.status_code == 401


def test_authenticated_user_can_create_ingredient(client):
    client.post(
        "/auth/register",
        json={
            "nombre": "Ángel",
            "email": "angel@example.com",
            "password": "secret123",
        },
    )
    login = client.post(
        "/auth/login",
        json={
            "email": "angel@example.com",
            "password": "secret123",
        },
    )
    token = login.json()["access_token"]

    response = client.post(
        "/ingredients/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Arroz",
            "cantidad": 2,
            "unidad": "tazas",
        },
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Arroz"
