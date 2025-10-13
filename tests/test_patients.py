import json

def test_add_patient(client, token):
    response = client.post(
        "/patients/",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"name": "Bob", "age": 40, "diagnosis": "Diabetes"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "id" in data

def test_create_patient_missing_field(client, auth_headers):
    response = client.post("/patients/", json={"name": "Bob"}, headers=auth_headers)
    assert response.status_code == 400

def test_get_non_existing_patient(client, auth_headers):
    response = client.get("/patients/999", headers=auth_headers)
    assert response.status_code == 404
