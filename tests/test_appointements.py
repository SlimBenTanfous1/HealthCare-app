import pytest

def test_create_appointment(client, auth_headers):
    data = {"patient_id": 1, "date": "2025-10-15", "reason": "Consultation"}
    response = client.post("/appointments/", json=data, headers=auth_headers)
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_get_appointments(client, auth_headers):
    response = client.get("/appointments/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_create_appointment_invalid(client, auth_headers):
    # patient_id manquant → erreur
    data = {"date": "2025-10-15"}
    response = client.post("/appointments/", json=data, headers=auth_headers)
    assert response.status_code == 400
