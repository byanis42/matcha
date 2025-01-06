# services/notification_service/application/notification_service.py

from sqlalchemy.orm import Session
from datetime import datetime
from services.notification_service.domain.models import Notification

def create_notification(
    db: Session,
    user_id: int,
    event_type: str,
    content: str = None,
    trigger_user_id: int = None
):
    """
    Crée une nouvelle notification pour 'user_id'.
    ex. event_type='like', content="User123 liked your profile"
    """
    notif = Notification(
        user_id=user_id,
        event_type=event_type,
        content=content,
        trigger_user_id=trigger_user_id
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def get_notifications(db: Session, user_id: int, unread_only: bool = False):
    """
    Récupère la liste des notifications d'un user.
    Si unread_only=True, filtre sur is_read=False.
    """
    query = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.is_read == False)
    return query.order_by(Notification.created_at.desc()).all()

def mark_notification_read(db: Session, notification_id: int):
    """
    Marque la notif comme lue, renvoie la notif mise à jour.
    """
    notif = db.query(Notification).filter(Notification.id == notification_id).one_or_none()
    if not notif:
        return None
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif

def mark_all_read(db: Session, user_id: int):
    """
    Marque TOUTES les notif d'un user comme lues.
    """
    db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update({"is_read": True})
    db.commit()
