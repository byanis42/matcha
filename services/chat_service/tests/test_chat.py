# services/chat_service/tests/test_chat.py

import pytest
from fastapi.testclient import TestClient
from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.sql import text  # <-- pour déclarer les requêtes textuelles

from services.chat_service.interface.main import app

# On importe la fonction check_if_connected pour la "patcher"
from services.chat_service.application.chat_service import check_if_connected

# On importe l'accès DB pour la fixture
from services.chat_service.infrastructure.database import get_session
from services.chat_service.domain.models import ChatMessage

client = TestClient(app)


@contextmanager
def get_db_sync():
    """
    Permet d'utiliser le générateur get_session() dans un with Python.
    """
    gen = get_session()
    db = next(gen)  # on récupère la session
    try:
        yield db
    finally:
        db.close()


def mock_check_if_connected(u1, u2):
    """
    Simule que les deux utilisateurs sont mutuellement connectés (mutual like).
    """
    return True


@pytest.fixture
def patch_connection(mocker):
    """
    Patch la fonction 'check_if_connected'
    pour qu'elle renvoie toujours True.
    """
    mocker.patch(
        "services.chat_service.application.chat_service.check_if_connected",
        side_effect=mock_check_if_connected
    )


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """
    Supprime toutes les entrées de chat_messages via TRUNCATE
    avant ET après chaque test,
    afin d'éviter l'accumulation de messages résiduels.
    """
    def truncate_table():
        with get_db_sync() as db:
            # On déclare la requête sous forme textuelle:
            # 'TRUNCATE TABLE chat_messages RESTART IDENTITY CASCADE;'
            # puis on l'enveloppe dans text(...)
            truncate_sql = text("TRUNCATE TABLE chat_messages RESTART IDENTITY CASCADE")
            db.execute(truncate_sql)
            db.commit()

    # Avant le test
    truncate_table()
    yield
    # Après le test
    truncate_table()


def test_send_and_get_messages(patch_connection):
    """
    Test qui vérifie :
    1) L'envoi d'un message (POST /messages)
    2) La récupération de la conversation (GET /messages/{user1}/{user2})
    3) Le marquage comme lu (PUT /messages/{msg_id}/read)
    """
    # 1) Envoi d'un message
    data = {
        "from_user_id": 123,
        "to_user_id": 456,
        "content": "Hello!"
    }
    resp = client.post("/messages", json=data)
    assert resp.status_code == 200, f"Envoi message échoué: {resp.text}"
    msg = resp.json()
    assert msg["content"] == "Hello!"
    assert msg["is_read"] is False

    # 2) Récupération de la conversation
    conv_resp = client.get("/messages/123/456")
    assert conv_resp.status_code == 200, f"Conversation échouée: {conv_resp.text}"
    conv = conv_resp.json()

    # On s'attend à 1 seul message pour ce test
    assert len(conv) == 1, f"Attendu 1 message, trouvé {len(conv)}: {conv}"
    assert conv[0]["content"] == "Hello!"
    assert conv[0]["is_read"] is False

    # 3) Marquage comme lu
    msg_id = conv[0]["id"]
    mark_resp = client.put(f"/messages/{msg_id}/read?user_id=456")
    assert mark_resp.status_code == 200, f"Marquage lu échoué: {mark_resp.text}"
    updated_msg = mark_resp.json()
    assert updated_msg["is_read"] is True
