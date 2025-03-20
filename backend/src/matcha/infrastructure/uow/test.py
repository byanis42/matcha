from matcha.domain.uow import MatchaUnitOfWork
from matcha.infrastructure.services.mocks.auth_service import MockAuthService
from matcha.infrastructure.services.mocks.email_service import MockEmailService
from matcha.infrastructure.services.mocks.storage_service import MockStorageService
from matcha.infrastructure.services.mocks.geolocation_service import MockGeolocationService
from matcha.infrastructure.services.mocks.message_bus import MockMessageBus
from matcha.infrastructure.services.mocks.notifications_service import MockNotificationsService
from matcha.infrastructure.repositories.mocks.user_repository import InMemoryUserRepository
from matcha.infrastructure.repositories.mocks.profile_repository import InMemoryProfileRepository
from matcha.infrastructure.repositories.mocks.matching_repository import InMemoryMatchingRepository
from matcha.infrastructure.repositories.mocks.chat_repository import InMemoryChatRepository
from matcha.infrastructure.repositories.mocks.notification_repository import InMemoryNotificationRepository


class InMemoryUnitOfWork(MatchaUnitOfWork):
    """
    In-memory implementation of the Unit of Work pattern for testing.
    Uses in-memory repositories and mock services.
    """

    def __init__(self):
        # Initialize state tracking
        self.committed = False
        self.rolled_back = False

        # Initialize mock services
        self.auth_service = MockAuthService()
        self.email_service = MockEmailService()
        self.storage_service = MockStorageService()
        self.geolocation_service = MockGeolocationService()
        self.message_bus = MockMessageBus(self)
        self.notifications_service = MockNotificationsService()

        # Initialize in-memory repositories
        self.user_repository = InMemoryUserRepository()
        self.profile_repository = InMemoryProfileRepository()
        self.matching_repository = InMemoryMatchingRepository()
        self.chat_repository = InMemoryChatRepository()
        self.notification_repository = InMemoryNotificationRepository()

    async def begin(self):
        """Start a new "transaction" (resets state)."""
        self.committed = False
        self.rolled_back = False

    async def commit(self):
        """Mark the UoW as committed and process queued domain events."""
        self.committed = True
        await self.message_bus.handle_events()

    async def rollback(self):
        """Mark the UoW as rolled back and clear event queue."""
        self.rolled_back = True
        await self.message_bus.clear_queue()
