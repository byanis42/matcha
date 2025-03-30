from pydantic import BaseModel, EmailStr


class CreateAccount(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    confirm_password: str


class ActivateAccount(BaseModel):
    activation_token: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str


class UpdateAccount(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None


class Login(BaseModel):
    email: EmailStr
    password: str
