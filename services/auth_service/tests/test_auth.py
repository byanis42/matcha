# services/auth_service/tests/test_auth.py

import random
import pytest
from fastapi.testclient import TestClient

from services.auth_service.interface.main import app

client = TestClient(app)

@pytest.fixture
def unique_user():
    """
    Crée un utilisateur unique via l'endpoint /register,
    puis le supprime après le test.
    """

    # 1) Générer des données uniques (pour éviter "already registered")
    random_id = random.randint(100000, 999999)
    user_data = {
        "email": f"user{random_id}@example.com",
        "username": f"user_{random_id}",
        "first_name": "Test",
        "last_name": "User",
        "password": "strongpassword"
    }

    # 2) Appeler /register pour créer l'utilisateur
    register_res = client.post("/register", json=user_data)
    # On s'attend à 200 si tout va bien (ou 201, selon votre API)
    assert register_res.status_code == 200, f"Register failed: {register_res.text}"

    # 3) On "yield" user_data pour que le test utilise ces infos
    yield user_data

    # 4) Nettoyage : supprimer l'utilisateur en base
    #    - Soit vous avez un endpoint /delete_user
    #    - Soit vous faites la suppression directe en base
    from sqlalchemy.orm import Session
    from services.auth_service.infrastructure.database import engine
    from services.auth_service.domain.models import User

    with Session(engine) as session:
        user_in_db = session.query(User).filter_by(username=user_data["username"]).one_or_none()
        if user_in_db:
            session.delete(user_in_db)
            session.commit()

def test_register_and_login(unique_user):
    """
    Teste que l'utilisateur, une fois créé, peut se connecter.
    """
    # L'utilisateur a été créé par la fixture unique_user
    user_data = unique_user

    # 1) Tester le login avec /login
    login_res = client.post("/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"

    data = login_res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
