import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    # ⚡ Override toute config par défaut
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret",
    })

    with app.app_context():
        db.drop_all()   # reset propre
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

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

