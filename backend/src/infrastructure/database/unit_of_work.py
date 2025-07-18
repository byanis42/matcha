from sqlalchemy.ext.asyncio import AsyncSession

from ...core.repositories.unit_of_work import AbstractUnitOfWork
from .repositories.user_repository_impl import UserRepositoryImpl


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """SQLAlchemy implementation of Unit of Work"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.users = UserRepositoryImpl(self.session)
        # Initialize other repositories here when we add them
        # self.user_profiles = UserProfileRepositoryImpl(self.session)
        # self.matchings = MatchingRepositoryImpl(self.session)
        # self.chats = ChatRepositoryImpl(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self) -> None:
        """Commit the current transaction"""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction"""
        await self.session.rollback()
