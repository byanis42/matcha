from typing import Dict, Any
from datetime import datetime

from ....core.entities.user import User, UserStatus
from ....core.value_objects.email import Email
from ....core.repositories.user_repository import UserRepository
from ....shared.exceptions import AuthenticationException, ValidationException
from ....shared.security import verify_password, create_access_token, create_refresh_token


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, login_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate user and return tokens
        """
        try:
            # Get user by email or username
            user = None
            if "@" in login_data["identifier"]:
                # Login with email
                user = await self.user_repository.get_by_email(login_data["identifier"])
            else:
                # Login with username
                user = await self.user_repository.get_by_username(login_data["identifier"])
            
            if not user:
                raise AuthenticationException("Invalid credentials")
            
            # Verify password
            if not verify_password(login_data["password"], user.password_hash):
                raise AuthenticationException("Invalid credentials")
            
            # Check user status
            if user.status == UserStatus.BANNED:
                raise AuthenticationException("Account is banned")
            
            if user.status == UserStatus.PENDING_VERIFICATION:
                raise AuthenticationException("Please verify your email first")
            
            if user.status == UserStatus.INACTIVE:
                raise AuthenticationException("Account is inactive")
            
            # Update last seen
            user.update_last_seen()
            await self.user_repository.update(user)
            
            # Generate tokens
            access_token = create_access_token({"user_id": user.id, "email": str(user.email)})
            refresh_token = create_refresh_token({"user_id": user.id})
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": str(user.email),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "status": user.status.value,
                    "last_seen": user.last_seen.isoformat() if user.last_seen else None
                }
            }
            
        except AuthenticationException:
            raise
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")