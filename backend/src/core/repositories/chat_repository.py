from abc import ABC, abstractmethod

from src.core.entities.chat import Conversation, Message, Notification


class ChatRepository(ABC):
    """Abstract repository for chat-related operations"""

    @abstractmethod
    async def create_conversation(self, conversation: Conversation) -> Conversation:
        """Create a new conversation"""
        pass

    @abstractmethod
    async def get_conversation_by_id(self, conversation_id: int) -> Conversation | None:
        """Get conversation by ID"""
        pass

    @abstractmethod
    async def get_conversation_by_match(self, match_id: int) -> Conversation | None:
        """Get conversation by match ID"""
        pass

    @abstractmethod
    async def get_conversations_by_user(self, user_id: int) -> list[Conversation]:
        """Get all conversations for a user"""
        pass

    @abstractmethod
    async def update_conversation(self, conversation: Conversation) -> Conversation:
        """Update conversation"""
        pass

    @abstractmethod
    async def delete_conversation(self, conversation_id: int) -> bool:
        """Delete conversation"""
        pass

    @abstractmethod
    async def send_message(self, message: Message) -> Message:
        """Send a message"""
        pass

    @abstractmethod
    async def get_message_by_id(self, message_id: int) -> Message | None:
        """Get message by ID"""
        pass

    @abstractmethod
    async def get_messages_by_conversation(
        self, conversation_id: int, limit: int = 50, offset: int = 0
    ) -> list[Message]:
        """Get messages in a conversation with pagination"""
        pass

    @abstractmethod
    async def get_messages_by_user(self, user_id: int) -> list[Message]:
        """Get all messages sent by a user"""
        pass

    @abstractmethod
    async def update_message(self, message: Message) -> Message:
        """Update message"""
        pass

    @abstractmethod
    async def delete_message(self, message_id: int) -> bool:
        """Delete message"""
        pass

    @abstractmethod
    async def mark_messages_as_read(self, conversation_id: int, user_id: int) -> bool:
        """Mark all messages in conversation as read for user"""
        pass

    @abstractmethod
    async def get_unread_message_count(self, user_id: int) -> int:
        """Get count of unread messages for user"""
        pass


class NotificationRepository(ABC):
    """Abstract repository for notification operations"""

    @abstractmethod
    async def create_notification(self, notification: Notification) -> Notification:
        """Create a new notification"""
        pass

    @abstractmethod
    async def get_notification_by_id(self, notification_id: int) -> Notification | None:
        """Get notification by ID"""
        pass

    @abstractmethod
    async def get_notifications_by_user(
        self, user_id: int, limit: int = 50, offset: int = 0
    ) -> list[Notification]:
        """Get notifications for a user with pagination"""
        pass

    @abstractmethod
    async def get_unread_notifications(self, user_id: int) -> list[Notification]:
        """Get unread notifications for a user"""
        pass

    @abstractmethod
    async def update_notification(self, notification: Notification) -> Notification:
        """Update notification"""
        pass

    @abstractmethod
    async def delete_notification(self, notification_id: int) -> bool:
        """Delete notification"""
        pass

    @abstractmethod
    async def mark_as_read(self, notification_id: int) -> bool:
        """Mark notification as read"""
        pass

    @abstractmethod
    async def mark_all_as_read(self, user_id: int) -> bool:
        """Mark all notifications as read for user"""
        pass

    @abstractmethod
    async def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications for user"""
        pass

    @abstractmethod
    async def delete_old_notifications(self, days: int = 30) -> int:
        """Delete notifications older than specified days"""
        pass
