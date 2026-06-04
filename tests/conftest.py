import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# We MUST patch app.database BEFORE anything else imports it
from app.database import Base, get_db

# Test database — use a file to persist across the test session
TEST_DATABASE_URL = "sqlite:///./test_recipes.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Patch the app's database engine
import app.database as db_module
db_module.engine = test_engine
db_module.SessionLocal = TestingSessionLocal

# Create tables on test engine
Base.metadata.create_all(bind=test_engine)

# Import app after setting up test DB
from app.main import app

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply dependency override
app.dependency_overrides[get_db] = override_get_db

# Clear tables before tests to ensure clean state
from sqlalchemy import text

def clear_tables():
    with test_engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(text("DELETE FROM calificaciones"))
            conn.execute(text("DELETE FROM recetas"))
            conn.execute(text("DELETE FROM ingredientes"))
            conn.execute(text("DELETE FROM usuarios"))
            trans.commit()
        except Exception:
            trans.rollback()

@pytest.fixture(scope="function")
def api_client():
    clear_tables()
    client = TestClient(app)
    yield client
    clear_tables()

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user():
    return {
        "nombre": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    }

@pytest.fixture
def auth_token(api_client, test_user):
    api_client.post("/auth/register", json=test_user)
    response = api_client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    return response.json()["access_token"]
