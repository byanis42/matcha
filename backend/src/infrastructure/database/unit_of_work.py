from sqlalchemy.ext.asyncio import AsyncSession

from ...core.repositories.unit_of_work import AbstractUnitOfWork
from ..external.email.smtp_email_service import SMTPEmailService
from .repositories.user_repository_impl import UserRepositoryImpl
from .repositories.verification_token_repository_impl import (
    VerificationTokenRepositoryImpl,
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """SQLAlchemy implementation of Unit of Work"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.users = UserRepositoryImpl(self.session)
        self.verification_tokens = VerificationTokenRepositoryImpl(self.session)
        self.email_service = SMTPEmailService()
        # Initialize other repositories here when we add them
        # self.user_profiles = UserProfileRepositoryImpl(self.session)
        # self.matchings = MatchingRepositoryImpl(self.session)
        # self.chats = ChatRepositoryImpl(self.session)
        await super().__aenter__()  # type: ignore[misc]
        return self

    async def __aexit__(self, *args: object) -> None:
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self) -> None:
        """Commit the current transaction"""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction"""
        await self.session.rollback()
