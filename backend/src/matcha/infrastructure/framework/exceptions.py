class DomainException(Exception):
    status_code: int = 500
    detail: str = "An error occurred"
    name: str = "Domain Exception"


class HandlerNotFound(DomainException):
    name: str = "Handler Not Found"
