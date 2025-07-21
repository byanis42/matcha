from abc import ABC, abstractmethod

from src.core.entities.verification_token import TokenType, VerificationToken


class VerificationTokenRepository(ABC):
    """Abstract verification token repository"""

    @abstractmethod
    async def create(self, token: VerificationToken) -> VerificationToken:
        """Create a new verification token"""
        pass

    @abstractmethod
    async def get_by_token(self, token: str) -> VerificationToken | None:
        """Get verification token by token string"""
        pass

    @abstractmethod
    async def get_valid_token(
        self, user_id: int, token_type: TokenType
    ) -> VerificationToken | None:
        """Get valid (not expired, not used) token for user and type"""
        pass

    @abstractmethod
    async def update(self, token: VerificationToken) -> VerificationToken:
        """Update verification token"""
        pass

    @abstractmethod
    async def delete_expired_tokens(self) -> int:
        """Delete all expired tokens and return count"""
        pass

    @abstractmethod
    async def invalidate_user_tokens(self, user_id: int, token_type: TokenType) -> int:
        """Invalidate all tokens for a user of a specific type"""
        pass
