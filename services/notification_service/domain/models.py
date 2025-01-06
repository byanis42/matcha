# services/notification_service/domain/models.py

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Notification(Base):
    """
    Représente une notification (chapitre IV.7).
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    # ex. 'like', 'view', 'message', 'likeback', 'unlike'
    event_type = Column(String, nullable=False)
    content = Column(String, nullable=True)        # ex. "User123 liked your profile"
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Optionnel: qui a déclenché la notif (ex. "UserXYZ a liké...")
    trigger_user_id = Column(Integer, nullable=True)
