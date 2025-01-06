# services/chat_service/application/chat_service.py

import httpx
from sqlalchemy.orm import Session
from services.chat_service.domain.models import ChatMessage
from datetime import datetime

LIKE_SERVICE_URL = "http://profile_service:8000"
# Ou un service dédié "like_service"

def check_if_connected(user1_id: int, user2_id: int) -> bool:
    """
    Vérifie si user1 et user2 sont "connectés" =>
    c.-à-d. user1 like user2 ET user2 like user1.
    Suppose un endpoint /likes/connected?u1=..&u2=.. => bool
    """
    try:
        resp = httpx.get(f"{LIKE_SERVICE_URL}/likes/connected", params={
            "u1": user1_id,
            "u2": user2_id
        })
        resp.raise_for_status()
        data = resp.json()  # on s'attend à { "connected": True/False }
        return data.get("connected", False)
    except:
        return False

def send_message(db: Session, from_user_id: int, to_user_id: int, content: str):
    """
    Envoie un message (sauvegarde en DB) seulement si 'connected'.
    """
    # Vérif connexion
    if not check_if_connected(from_user_id, to_user_id):
        raise ValueError("Users are not connected (mutual like).")

    msg = ChatMessage(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        content=content,
        timestamp=datetime.utcnow(),
        is_read=False
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_conversation(db: Session, user1_id: int, user2_id: int):
    """
    Récupère tous les messages entre user1_id et user2_id,
    triés par timestamp.
    """
    # On peut vérifier la connexion, mais pas forcément obligatoire
    # si la lecture est autorisée même sans connexion.
    msgs = db.query(ChatMessage).filter(
        ((ChatMessage.from_user_id == user1_id) & (ChatMessage.to_user_id == user2_id)) |
        ((ChatMessage.from_user_id == user2_id) & (ChatMessage.to_user_id == user1_id))
    ).order_by(ChatMessage.timestamp.asc()).all()

    return msgs

def mark_as_read(db: Session, message_id: int, user_id: int):
    """
    Marque un message comme lu,
    seulement si 'user_id' est le destinataire.
    """
    msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).one_or_none()
    if not msg:
        return None

    if msg.to_user_id != user_id:
        raise ValueError("User not authorized to mark this message as read.")

    msg.is_read = True
    db.commit()
    db.refresh(msg)
    return msg
