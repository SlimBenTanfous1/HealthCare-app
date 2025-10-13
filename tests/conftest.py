import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token(client):
    client.post("/auth/register", json={"username": "tester", "password": "1234"})
    res = client.post("/auth/login", json={"username": "tester", "password": "1234"})
    return res.get_json()["access_token"]
