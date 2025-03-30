from pydantic import EmailStr
from matcha.infrastructure.framework.models import Command


class CreateAccount(Command):
    name: str
    surname: str
    email: EmailStr
    password: str
    confirm_password: str
