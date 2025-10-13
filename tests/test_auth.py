import json

def test_register_and_login(client):
    # Test register
    response = client.post(
        "/auth/register",
        data=json.dumps({"username": "testuser", "password": "testpass"}),
        content_type="application/json",
    )
    assert response.status_code in [200, 201]

    # Test login
    response = client.post(
        "/auth/login",
        data=json.dumps({"username": "testuser", "password": "testpass"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data

def test_register_existing_user(client):
    response = client.post("/auth/register", json={"username": "slim", "password": "test"})
    assert response.status_code == 400
    assert "already exists" in response.get_json()["error"]

def test_login_invalid(client):
    response = client.post("/auth/login", json={"username": "ghost", "password": "wrong"})
    assert response.status_code == 401
