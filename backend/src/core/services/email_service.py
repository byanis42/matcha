from abc import ABC, abstractmethod


class EmailService(ABC):
    """Abstract email service interface"""

    @abstractmethod
    async def send_verification_email(
        self, email: str, username: str, token: str
    ) -> bool:
        """Send email verification email"""
        pass

    @abstractmethod
    async def send_password_reset_email(
        self, email: str, username: str, token: str
    ) -> bool:
        """Send password reset email"""
        pass

    @abstractmethod
    async def send_notification_email(
        self, email: str, subject: str, message: str
    ) -> bool:
        """Send a general notification email"""
        pass
