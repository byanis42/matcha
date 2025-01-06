# services/chat_service/domain/models.py

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class ChatMessage(Base):
    """
    Stocke les messages entre utilisateurs "connectés".
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, nullable=False)
    to_user_id = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
