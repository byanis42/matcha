from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text

from ..session import Base


class ConversationModel(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="active")
    last_message_id = Column(Integer, nullable=True)
    last_message_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")
    status = Column(String(20), default="sent")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)


class NotificationModel(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(20), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(String(20), default="medium")
    read = Column(Boolean, default=False)
    related_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    related_entity_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
