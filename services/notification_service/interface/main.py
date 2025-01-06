# services/notification_service/interface/main.py

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.notification_service.infrastructure.database import init_db, get_session
from services.notification_service.application.notification_service import (
    create_notification,
    get_notifications,
    mark_notification_read,
    mark_all_read
)

app = FastAPI()

# Créer les tables au démarrage (en dev/test)
init_db()

# Schémas Pydantic

class NotificationCreate(BaseModel):
    user_id: int
    event_type: str
    content: str | None = None
    trigger_user_id: int | None = None

class NotificationOut(BaseModel):
    id: int
    user_id: int
    event_type: str
    content: str | None
    is_read: bool
    trigger_user_id: int | None = None

    class Config:
        orm_mode = True

# Endpoints

@app.post("/notifications", response_model=NotificationOut)
def create_notification_endpoint(data: NotificationCreate, db: Session = Depends(get_session)):
    notif = create_notification(
        db=db,
        user_id=data.user_id,
        event_type=data.event_type,
        content=data.content,
        trigger_user_id=data.trigger_user_id
    )
    return notif

@app.get("/notifications", response_model=list[NotificationOut])
def get_notifications_endpoint(
    user_id: int,
    unread_only: bool = False,
    db: Session = Depends(get_session)
):
    notifs = get_notifications(db, user_id, unread_only)
    return notifs

@app.put("/notifications/{notification_id}/read", response_model=NotificationOut)
def mark_notification_read_endpoint(notification_id: int, db: Session = Depends(get_session)):
    notif = mark_notification_read(db, notification_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return notif

@app.put("/notifications/readall")
def mark_all_read_endpoint(user_id: int, db: Session = Depends(get_session)):
    mark_all_read(db, user_id)
    return {"detail": "All notifications marked as read."}
