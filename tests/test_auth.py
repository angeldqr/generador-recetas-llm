import pytest


def test_register_user(api_client, test_user):
    """Test user registration endpoint."""
    response = api_client.post("/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["nombre"] == test_user["nombre"]
    assert "id" in data


def test_register_duplicate_email(api_client, test_user):
    """Test that registering with duplicate email fails."""
    api_client.post("/auth/register", json=test_user)
    response = api_client.post("/auth/register", json=test_user)
    assert response.status_code == 400
    assert "correo" in response.json()["detail"].lower()


def test_login_user(api_client, test_user):
    """Test user login returns valid JWT token."""
    api_client.post("/auth/register", json=test_user)
    response = api_client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(api_client, test_user):
    """Test login with wrong password fails."""
    api_client.post("/auth/register", json=test_user)
    response = api_client.post("/auth/login", json={
        "email": test_user["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
