from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(v) > 50:
            raise ValueError("Username cannot exceed 50 characters")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v):
        if not v or len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(v) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        return v.strip().title()


class UserLoginRequest(BaseModel):
    identifier: str  # email or username
    password: str

    @field_validator("identifier")
    @classmethod
    def validate_identifier(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Email or username is required")
        return v.lower()


class EmailVerificationRequest(BaseModel):
    user_id: int
    token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirmRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class TokenRefreshRequest(BaseModel):
    refresh_token: str


# Response schemas
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    status: str
    email_verified: bool
    last_seen: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RegisterResponse(BaseModel):
    message: str
    user_id: int
    email: str
    username: str
    verification_token: str


class VerificationResponse(BaseModel):
    message: str
    user_id: int
    status: str
    email_verified: bool


class PasswordResetResponse(BaseModel):
    message: str
    email: str
    reset_token: str | None = None  # Only for development


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None
