from datetime import datetime, timedelta
from enum import Enum

from pydantic import BaseModel, ConfigDict


class TokenType(str, Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"


class VerificationToken(BaseModel):
    """Verification token entity"""

    model_config = ConfigDict(use_enum_values=True)

    id: int | None = None
    user_id: int
    token: str
    token_type: TokenType
    expires_at: datetime
    used: bool = False
    created_at: datetime | None = None

    def is_expired(self) -> bool:
        """Check if token is expired"""
        return datetime.utcnow() > self.expires_at

    def is_valid(self) -> bool:
        """Check if token is valid (not expired and not used)"""
        return not self.used and not self.is_expired()

    def use_token(self) -> None:
        """Mark token as used"""
        self.used = True

    @classmethod
    def create_email_verification_token(cls, user_id: int, token: str) -> "VerificationToken":
        """Create an email verification token"""
        expires_at = datetime.utcnow() + timedelta(hours=24)  # 24 hours
        return cls(
            user_id=user_id,
            token=token,
            token_type=TokenType.EMAIL_VERIFICATION,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )

    @classmethod
    def create_password_reset_token(cls, user_id: int, token: str) -> "VerificationToken":
        """Create a password reset token"""
        expires_at = datetime.utcnow() + timedelta(hours=1)  # 1 hour
        return cls(
            user_id=user_id,
            token=token,
            token_type=TokenType.PASSWORD_RESET,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
