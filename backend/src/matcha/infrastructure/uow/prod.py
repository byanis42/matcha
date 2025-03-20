import asyncpg
from matcha.domain.uow import MatchaUnitOfWork
from matcha.infrastructure.services.auth_service import AuthService
from matcha.infrastructure.services.email_service import EmailService
from matcha.infrastructure.services.storage_service import StorageService
from matcha.infrastructure.services.geolocation_service import GeolocationService
from matcha.infrastructure.services.message_bus import MessageBus
from matcha.infrastructure.services.notifications_service import NotificationsService
from matcha.infrastructure.repositories.user_repository import PostgresUserRepository
from matcha.infrastructure.repositories.profile_repository import PostgresProfileRepository
from matcha.infrastructure.repositories.matching_repository import PostgresMatchingRepository
from matcha.infrastructure.repositories.chat_repository import PostgresChatRepository
from matcha.infrastructure.repositories.notification_repository import PostgresNotificationRepository


class PostgresUnitOfWork(MatchaUnitOfWork):
    """
    PostgreSQL implementation of the Unit of Work pattern for production environment.
    Handles transaction boundaries and provides access to repositories and services.
    """

    def __init__(self, connection_string: str):
        # Connection info
        self.connection_string = connection_string
        self.connection = None
        self.transaction = None

        # Initialize services
        self.auth_service = AuthService()
        self.email_service = EmailService()
        self.storage_service = StorageService()
        self.geolocation_service = GeolocationService()
        self.message_bus = MessageBus(self)
        self.notifications_service = NotificationsService()

        # Repositories will be initialized during begin()
        self.user_repository = None
        self.profile_repository = None
        self.matching_repository = None
        self.chat_repository = None
        self.notification_repository = None

    async def bootstrap_repos(self):
        """Initialize repositories with the active connection."""
        self.user_repository = PostgresUserRepository(self.connection)
        self.profile_repository = PostgresProfileRepository(self.connection)
        self.matching_repository = PostgresMatchingRepository(self.connection)
        self.chat_repository = PostgresChatRepository(self.connection)
        self.notification_repository = PostgresNotificationRepository(self.connection)

    async def begin(self):
        """Start a new database transaction."""
        self.connection = await asyncpg.connect(self.connection_string)
        await self.bootstrap_repos()
        self.transaction = self.connection.transaction()
        await self.transaction.start()

    async def commit(self):
        """Commit the transaction and process queued domain events."""
        await self.transaction.commit()
        await self.connection.close()
        await self.message_bus.handle_events()

    async def rollback(self):
        """Rollback the transaction and clear the event queue."""
        await self.transaction.rollback()
        await self.connection.close()
        await self.message_bus.clear_queue()
