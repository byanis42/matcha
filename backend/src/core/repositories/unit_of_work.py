from abc import ABC, abstractmethod
from typing import Any

from src.core.repositories.profile_repository import ProfileRepository
from src.core.repositories.user_repository import UserRepository
from src.core.repositories.verification_token_repository import (
    VerificationTokenRepository,
)
from src.core.services.email_service import EmailService


class AbstractUnitOfWork(ABC):
    """Abstract Unit of Work interface"""

    users: UserRepository
    verification_tokens: VerificationTokenRepository
    profiles: ProfileRepository
    email_service: EmailService
    # matchings: MatchingRepository
    # chats: ChatRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args: Any) -> None:
        self.rollback()

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction"""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction"""
        raise NotImplementedError
