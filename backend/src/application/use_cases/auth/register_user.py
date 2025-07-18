import secrets
from datetime import datetime
from typing import Any

from pydantic import ValidationError

from ....core.entities.user import User, UserStatus
from ....core.entities.verification_token import VerificationToken
from ....core.repositories.unit_of_work import AbstractUnitOfWork
from ....core.value_objects.email import Email
from ....shared.exceptions import DuplicateResourceException, ValidationException
from ....shared.security import hash_password


class RegisterUserUseCase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, user_data: dict[str, Any]) -> dict[str, Any]:
        """
        Register a new user with email verification
        """
        try:
            async with self.uow:
                # Validate input data
                email = Email(user_data["email"])

                # Check if user already exists
                if await self.uow.users.exists_by_email(str(email)):
                    raise DuplicateResourceException("Email already registered")

                if await self.uow.users.exists_by_username(user_data["username"]):
                    raise DuplicateResourceException("Username already taken")

                # Hash password
                password_hash = hash_password(user_data["password"])

                # Create user entity
                user = User(
                    username=user_data["username"],
                    email=email,
                    password_hash=password_hash,
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    status=UserStatus.PENDING_VERIFICATION,
                    email_verified=False,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )

                # Save user to repository
                created_user = await self.uow.users.create(user)

                # Generate verification token
                verification_token_str = secrets.token_urlsafe(32)
                verification_token = VerificationToken.create_email_verification_token(
                    user_id=created_user.id,
                    token=verification_token_str
                )

                # Save verification token
                await self.uow.verification_tokens.create(verification_token)

                # Send verification email
                email_sent = await self.uow.email_service.send_verification_email(
                    email=str(created_user.email),
                    username=created_user.username,
                    token=verification_token_str
                )

                # Commit the transaction
                await self.uow.commit()

                return {
                    "user_id": created_user.id,
                    "email": str(created_user.email),
                    "username": created_user.username,
                    "verification_token": verification_token_str,
                    "email_sent": email_sent,
                    "message": "User registered successfully. Please check your email to verify your account.",
                }

        except ValidationError as e:
            raise ValidationException(f"Validation error: {str(e)}") from e
        except (DuplicateResourceException, ValidationException):
            # Re-raise domain exceptions as-is so they can be handled properly by the API layer
            raise
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}") from e
