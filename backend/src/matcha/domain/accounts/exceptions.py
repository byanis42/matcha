from matcha.infrastructure.framework.exceptions import DomainException

class PasswordsMismatch(DomainException):
    status_code: int = 400
    detail: str = "Passwords mismatch"
    name: str = "Passwords Mismatch"

class EmailAlreadyExists(DomainException):
    status_code: int = 400
    detail: str = "Email already exists"
    name: str = "Email Already Exists"
