# services/auth_service/tests/test_auth.py
from fastapi.testclient import TestClient
from services.auth_service.interface.main import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "strongpassword"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login():
    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "strongpassword"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
