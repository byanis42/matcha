from typing import Dict, Any
from datetime import datetime, timedelta
import secrets
from pydantic import ValidationError

from ....core.entities.user import User, UserStatus
from ....core.value_objects.email import Email
from ....core.repositories.user_repository import UserRepository
from ....shared.exceptions import ValidationException, DuplicateResourceException
from ....shared.security import hash_password


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new user with email verification
        """
        try:
            # Validate input data
            email = Email(user_data["email"])
            
            # Check if user already exists
            if await self.user_repository.exists_by_email(str(email)):
                raise DuplicateResourceException("Email already registered")
            
            if await self.user_repository.exists_by_username(user_data["username"]):
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
                updated_at=datetime.utcnow()
            )
            
            # Save user to repository
            created_user = await self.user_repository.create(user)
            
            # Generate verification token
            verification_token = secrets.token_urlsafe(32)
            
            return {
                "user_id": created_user.id,
                "email": str(created_user.email),
                "username": created_user.username,
                "verification_token": verification_token,
                "message": "User registered successfully. Please verify your email."
            }
            
        except ValidationError as e:
            raise ValidationException(f"Validation error: {str(e)}")
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")