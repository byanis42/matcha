from matcha.infrastructure.framework.uow import UnitOfWork


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
    user_repository: AbstractUserRepository
    profile_repository: AbstractProfileRepository
    matching_repository: AbstractMatchingRepository
    chat_repository: AbstractChatRepository
    notification_repository: AbstractNotificationRepository
