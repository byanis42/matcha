"""Custom exceptions for the Matcha application"""


class MatchaException(Exception):
    """Base exception for all Matcha-related errors"""

    pass


class ValidationException(MatchaException):
    """Raised when validation fails"""

    pass


class AuthenticationException(MatchaException):
    """Raised when authentication fails"""

    pass


class AuthorizationException(MatchaException):
    """Raised when authorization fails"""

    pass


class NotFoundException(MatchaException):
    """Raised when a resource is not found"""

    pass


class DuplicateResourceException(MatchaException):
    """Raised when trying to create a duplicate resource"""

    pass


class BusinessLogicException(MatchaException):
    """Raised when business logic validation fails"""

    pass


class ExternalServiceException(MatchaException):
    """Raised when an external service fails"""

    pass


class DatabaseException(MatchaException):
    """Raised when database operations fail"""

    pass


class RateLimitException(MatchaException):
    """Raised when rate limit is exceeded"""

    pass


class FileUploadException(MatchaException):
    """Raised when file upload fails"""

    pass


class GeolocationException(MatchaException):
    """Raised when geolocation operations fail"""

    pass


class NotificationException(MatchaException):
    """Raised when notification operations fail"""

    pass


class MatchingException(MatchaException):
    """Raised when matching operations fail"""

    pass


class ChatException(MatchaException):
    """Raised when chat operations fail"""

    pass
