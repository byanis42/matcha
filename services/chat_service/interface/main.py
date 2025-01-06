# services/chat_service/interface/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List
from sqlalchemy.orm import Session

from services.chat_service.infrastructure.database import init_db, get_session
from services.chat_service.application.chat_service import (
    send_message,
    get_conversation,
    mark_as_read,
    check_if_connected,
)
from services.chat_service.domain.models import ChatMessage

app = FastAPI()

# Initialisation de la DB (table chat_messages)
init_db()


# ===================== SCHÉMAS Pydantic =====================

class MessageCreate(BaseModel):
    from_user_id: int
    to_user_id: int
    content: str

class MessageOut(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    content: str
    is_read: bool

    class Config:
        orm_mode = True


# ===================== ENDPOINTS REST =====================

@app.post("/messages", response_model=MessageOut)
def send_message_endpoint(data: MessageCreate, db: Session = Depends(get_session)):
    """
    Envoie un message (stockage en DB), seulement si from_user et to_user sont "connectés" (mutual like).
    """
    try:
        msg = send_message(db, data.from_user_id, data.to_user_id, data.content)
        return msg
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/messages/{user1_id}/{user2_id}", response_model=List[MessageOut])
def get_conversation_endpoint(user1_id: int, user2_id: int, db: Session = Depends(get_session)):
    """
    Récupère l'ensemble des messages entre user1_id et user2_id.
    """
    msgs = get_conversation(db, user1_id, user2_id)
    return msgs

@app.put("/messages/{message_id}/read", response_model=MessageOut)
def mark_as_read_endpoint(message_id: int, user_id: int, db: Session = Depends(get_session)):
    """
    Marque un message comme lu, seulement si user_id est le destinataire (to_user_id).
    """
    try:
        msg = mark_as_read(db, message_id, user_id)
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found.")
        return msg
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===================== LOGIQUE WEBSOCKET =====================

# On garde un registre en mémoire des WebSocket connectées par user_id.
connected_websockets: Dict[int, WebSocket] = {}

@app.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket permettant à 'user_id' de recevoir/envoyer des messages en temps réel.
    Hypothèse: On peut faire un "send" via ce WebSocket pour l'autre user si "connected".
    """

    # On accepte la connexion
    await websocket.accept()

    # On stocke le WebSocket dans un registre
    connected_websockets[user_id] = websocket
    print(f"[WebSocket] user_id={user_id} connected.")

    try:
        while True:
            # On attend un message en provenance de user_id
            data = await websocket.receive_text()

            # On peut imaginer que 'data' contient un JSON du type:
            # {"to_user_id": 456, "content": "Hello!"}

            # Pour simplifier, on parse via JSON standard:
            import json
            try:
                payload = json.loads(data)
                to_user_id = payload.get("to_user_id")
                content = payload.get("content")

                # Vérifier la connexion mutuelle
                if not check_if_connected(user_id, to_user_id):
                    # Optionnel: on envoie un message d'erreur au WebSocket
                    await websocket.send_text("Not connected (mutual like) with this user.")
                    continue

                # Envoyer en base
                from services.chat_service.infrastructure.database import get_session
                # On ouvre une session DB "à la main" (pour l'exemple)
                # => dans un vrai code, on gèrerait peut-être autrement
                with get_session() as db_sess:
                    try:
                        msg_obj = send_message(db_sess, user_id, to_user_id, content)
                    except ValueError:
                        await websocket.send_text("Cannot send message: not connected or other error.")
                        continue

                # On envoie le message en temps réel au destinataire s'il est connecté
                if to_user_id in connected_websockets:
                    # construire un JSON
                    outgoing = {
                        "id": msg_obj.id,
                        "from_user_id": msg_obj.from_user_id,
                        "to_user_id": msg_obj.to_user_id,
                        "content": msg_obj.content,
                        "is_read": msg_obj.is_read,
                    }
                    await connected_websockets[to_user_id].send_text(json.dumps(outgoing))

                # On peut aussi informer l'émetteur que c'est "envoyé"
                await websocket.send_text("Message sent successfully.")

            except json.JSONDecodeError:
                await websocket.send_text("Invalid message format. Expected JSON.")

    except WebSocketDisconnect:
        print(f"[WebSocket] user_id={user_id} disconnected.")
    finally:
        # Retrait du registre
        if user_id in connected_websockets:
            del connected_websockets[user_id]
