from dataclasses import dataclass, field
from typing import Dict, List

from matcha.domain.uow import MatchaUnitOfWork
from matcha.infrastructure.framework.uow import UnitOfWork
from matcha.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from matcha.infrastructure.repositories.in_memory_profile_repository import InMemoryProfileRepository
from matcha.infrastructure.repositories.in_memory_matching_repository import InMemoryMatchingRepository
from matcha.infrastructure.repositories.in_memory_chat_repository import InMemoryChatRepository
from matcha.infrastructure.repositories.in_memory_notification_repository import InMemoryNotificationRepository
from matcha.infrastructure.services.test_auth import TestAuthService
from matcha.infrastructure.services.test_email import TestEmailService
from matcha.infrastructure.services.test_geolocation import TestGeolocationService
from matcha.infrastructure.services.test_storage import TestStorageService
from matcha.infrastructure.services.test_notification import TestNotificationService
from matcha.infrastructure.services.test_message_bus import TestMessageBus


@dataclass
class TestUnitOfWork(UnitOfWork, MatchaUnitOfWork):
    """
    Implémentation du UnitOfWork pour les tests, utilisant des repositories en mémoire
    et des services simulés.
    """
    # Suivi des événements et des messages pour les tests
    sent_emails: List[Dict] = field(default_factory=list)
    sent_notifications: List[Dict] = field(default_factory=list)
    processed_events: List[Dict] = field(default_factory=list)

    def __init__(self):
        # Services
        self.auth_service = TestAuthService()
        self.email_service = TestEmailService(self.sent_emails)
        self.storage_service = TestStorageService()
        self.geolocation_service = TestGeolocationService()
        self.message_bus = TestMessageBus(self, self.processed_events)
        self.notifications_service = TestNotificationService(self.sent_notifications)

        # Repositories
        self.account = InMemoryUserRepository()
        self.profile = InMemoryProfileRepository()
        self.matching = InMemoryMatchingRepository()
        self.chat = InMemoryChatRepository()
        self.notification = InMemoryNotificationRepository()

    async def begin(self):
        # Rien à faire pour les tests en mémoire
        pass

    async def commit(self):
        # Traiter les événements du domaine
        await self.message_bus.process_events()

    async def rollback(self):
        # Rien à faire pour les tests en mémoire
        pass
