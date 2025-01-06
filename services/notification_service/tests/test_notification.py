# services/notification_service/tests/test_notification.py

import random
from fastapi.testclient import TestClient
from services.notification_service.interface.main import app

client = TestClient(app)

def test_create_and_read_notification():
    # 1) Créer une notif
    user_id = random.randint(1000, 9999)
    data = {
        "user_id": user_id,
        "event_type": "like",
        "content": "User123 liked your profile"
    }

    resp = client.post("/notifications", json=data)
    assert resp.status_code == 200, f"Create notification failed: {resp.text}"
    notif = resp.json()
    assert notif["event_type"] == "like"
    assert notif["user_id"] == user_id
    assert notif["is_read"] == False

    # 2) Récupérer la liste (unread_only=False => doit contenir la notif)
    list_resp = client.get(f"/notifications?user_id={user_id}")
    assert list_resp.status_code == 200
    notifs = list_resp.json()
    assert len(notifs) > 0
    assert notifs[0]["id"] == notif["id"]

    # 3) Marquer la notif comme lue
    notif_id = notif["id"]
    mark_resp = client.put(f"/notifications/{notif_id}/read")
    assert mark_resp.status_code == 200
    updated = mark_resp.json()
    assert updated["is_read"] == True

    # 4) Vérifier la liste en unread_only => devrait être vide
    unread_resp = client.get(f"/notifications?user_id={user_id}&unread_only=true")
    unread_list = unread_resp.json()
    assert len(unread_list) == 0
