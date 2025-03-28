from typing import final
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from matcha.domain.uow import MatchaUnitOfWork
from matcha.infrastructure.framework.uow import UnitOfWork
from matcha.infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from matcha.infrastructure.repositories.postgres_profile_repository import PostgresProfileRepository
from matcha.infrastructure.repositories.postgres_matching_repository import PostgresMatchingRepository
from matcha.infrastructure.repositories.postgres_chat_repository import PostgresChatRepository
from matcha.infrastructure.repositories.postgres_notification_repository import PostgresNotificationRepository
from matcha.infrastructure.services.auth import AuthService
from matcha.infrastructure.services.email import EmailService
from matcha.infrastructure.services.geolocation import GeolocationService
from matcha.infrastructure.services.storage import StorageService
from matcha.infrastructure.services.notification import NotificationService
from matcha.infrastructure.services.message_bus import MessageBus


class PostgresUnitOfWork(UnitOfWork, MatchaUnitOfWork):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = create_async_engine(connection_string)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

        # Services
        self.auth_service = AuthService()
        self.email_service = EmailService()
        self.storage_service = StorageService()
        self.geolocation_service = GeolocationService()
        self.message_bus = MessageBus(self)
        self.notifications_service = NotificationService()

    async def bootstrap_repos(self, session: AsyncSession):
        self.account = PostgresUserRepository(session)
        self.profile = PostgresProfileRepository(session)
        self.matching = PostgresMatchingRepository(session)
        self.chat = PostgresChatRepository(session)
        self.notification = PostgresNotificationRepository(session)

    async def begin(self):
        self.session = self.session_factory()
        await self.bootstrap_repos(self.session)

    async def commit(self):
        await self.session.commit()
        await self.session.close()
        # Traiter les événements du domaine
        await self.message_bus.process_events()

    async def rollback(self):
        await self.session.rollback()
        await self.session.close()
