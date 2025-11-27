import os
import pytest
from app import create_app, db
from models import Patient


@pytest.fixture
def app():
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret",
    })

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Seed un patient par défaut pour tests
        db.session.add(Patient(name="John Doe", age=30, diagnosis="Healthy"))
        db.session.commit()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Register user if not exists
    client.post("/auth/register", json={"username": "test", "password": "test"})
    # Login to get token
    response = client.post("/auth/login", json={"username": "test", "password": "test"})
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}  


@pytest.fixture
def token(client):
    client.post("/auth/register", json={"username": "tokenuser", "password": "test"})
    response = client.post("/auth/login", json={"username": "tokenuser", "password": "test"})
    return response.get_json()["access_token"]

