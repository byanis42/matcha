# services/profile_service/tests/test_profile.py
import random
from fastapi.testclient import TestClient
from services.profile_service.interface.main import app

client = TestClient(app)

def test_create_and_get_profile():
    user_id = random.randint(1000, 9999)
    create_data = {
        "user_id": user_id,
        "gender": "M",
        "orientation": "hetero",
        "biography": "Just a test user",
        "interests": "#vegan,#geek",
        "pictures": "http://img1.com,http://img2.com"
    }

    resp = client.post("/profiles", json=create_data)
    assert resp.status_code == 200, f"Create profile failed: {resp.text}"
    profile = resp.json()
    assert profile["user_id"] == user_id

    # Récupérer le profil
    get_resp = client.get(f"/profiles/{user_id}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["biography"] == "Just a test user"
    assert fetched["pictures"] == "http://img1.com,http://img2.com"
