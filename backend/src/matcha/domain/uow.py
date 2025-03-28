from typing import Protocol

from matcha.infrastructure.framework.uow import UnitOfWork

from matcha.domain.services.auth import AbstractAuthService
from matcha.domain.services.email import AbstractEmailService
from matcha.domain.services.storage import AbstractStorageService
from matcha.domain.services.geolocation import AbstractGeolocationService
from matcha.domain.services.message_bus import AbstractMessageBus
from matcha.domain.services.notifications import AbstractNotificationsService

from matcha.domain.account.repository import AbstractAccountRepository
from matcha.domain.profile.repository import AbstractProfileRepository
from matcha.domain.matching.repository import AbstractMatchingRepository
from matcha.domain.chat.repository import AbstractChatRepository
from matcha.domain.notification.repository import AbstractNotificationRepository


class MatchaUnitOfWork(UnitOfWork):
    """
    Matcha-specific Unit of Work interface that defines all repositories
    and services needed for our application.
    """

    # Services
    auth_service: AbstractAuthService
    email_service: AbstractEmailService
    storage_service: AbstractStorageService
    geolocation_service: AbstractGeolocationService
    message_bus: AbstractMessageBus
    notifications_service: AbstractNotificationsService

    # Repositories
    account: AbstractAccountRepository
    profile: AbstractProfileRepository
    matching: AbstractMatchingRepository
    chat: AbstractChatRepository
    notification: AbstractNotificationRepository
