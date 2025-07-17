from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    EMOJI = "emoji"
    SYSTEM = "system"


class MessageStatus(str, Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class Message(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int | None = None
    conversation_id: int
    sender_id: int
    receiver_id: int
    content: str
    message_type: MessageType = MessageType.TEXT
    status: MessageStatus = MessageStatus.SENT
    created_at: datetime | None = None
    updated_at: datetime | None = None
    read_at: datetime | None = None
    
    @field_validator('conversation_id', 'sender_id', 'receiver_id')
    @classmethod
    def validate_ids(cls, v):
        if v <= 0:
            raise ValueError('ID must be positive')
        return v
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message content cannot be empty')
        if len(v) > 1000:
            raise ValueError('Message content cannot exceed 1000 characters')
        return v.strip()
    
    def mark_as_read(self) -> None:
        self.status = MessageStatus.READ
        self.read_at = datetime.utcnow()
    
    def mark_as_delivered(self) -> None:
        if self.status == MessageStatus.SENT:
            self.status = MessageStatus.DELIVERED
    
    def mark_as_failed(self) -> None:
        self.status = MessageStatus.FAILED
    
    def is_read(self) -> bool:
        return self.status == MessageStatus.READ
    
    def is_image(self) -> bool:
        return self.message_type == MessageType.IMAGE
    
    def is_system_message(self) -> bool:
        return self.message_type == MessageType.SYSTEM


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    BLOCKED = "blocked"
    DELETED = "deleted"


class Conversation(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int | None = None
    match_id: int
    user1_id: int
    user2_id: int
    status: ConversationStatus = ConversationStatus.ACTIVE
    last_message_id: int | None = None
    last_message_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    @field_validator('match_id', 'user1_id', 'user2_id')
    @classmethod
    def validate_ids(cls, v):
        if v <= 0:
            raise ValueError('ID must be positive')
        return v
    
    def involves_user(self, user_id: int) -> bool:
        return user_id in [self.user1_id, self.user2_id]
    
    def get_other_user_id(self, user_id: int) -> int | None:
        if user_id == self.user1_id:
            return self.user2_id
        elif user_id == self.user2_id:
            return self.user1_id
        return None
    
    def is_active(self) -> bool:
        return self.status == ConversationStatus.ACTIVE
    
    def archive(self) -> None:
        self.status = ConversationStatus.ARCHIVED
    
    def block(self) -> None:
        self.status = ConversationStatus.BLOCKED
    
    def delete(self) -> None:
        self.status = ConversationStatus.DELETED
    
    def update_last_message(self, message_id: int) -> None:
        self.last_message_id = message_id
        self.last_message_at = datetime.utcnow()


class NotificationType(str, Enum):
    LIKE = "like"
    SUPER_LIKE = "super_like"
    MATCH = "match"
    MESSAGE = "message"
    PROFILE_VISIT = "profile_visit"
    SYSTEM = "system"


class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Notification(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int | None = None
    user_id: int
    type: NotificationType
    title: str
    content: str
    priority: NotificationPriority = NotificationPriority.MEDIUM
    read: bool = False
    related_user_id: int | None = None
    related_entity_id: int | None = None
    created_at: datetime | None = None
    read_at: datetime | None = None
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        if v <= 0:
            raise ValueError('User ID must be positive')
        return v
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title cannot exceed 100 characters')
        return v.strip()
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Content cannot be empty')
        if len(v) > 500:
            raise ValueError('Content cannot exceed 500 characters')
        return v.strip()
    
    def mark_as_read(self) -> None:
        self.read = True
        self.read_at = datetime.utcnow()
    
    def is_read(self) -> bool:
        return self.read
    
    def is_urgent(self) -> bool:
        return self.priority == NotificationPriority.URGENT
    
    def is_match_notification(self) -> bool:
        return self.type == NotificationType.MATCH
    
    def is_message_notification(self) -> bool:
        return self.type == NotificationType.MESSAGE