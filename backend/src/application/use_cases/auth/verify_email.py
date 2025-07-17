from typing import Dict, Any
from datetime import datetime

from ....core.entities.user import User, UserStatus
from ....core.repositories.user_repository import UserRepository
from ....shared.exceptions import ValidationException, NotFoundException


class VerifyEmailUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, verification_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify user email with token
        """
        try:
            user_id = verification_data["user_id"]
            token = verification_data["token"]
            
            # Get user
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                raise NotFoundException("User not found")
            
            # Check if already verified
            if user.email_verified:
                return {
                    "message": "Email already verified",
                    "user_id": user.id,
                    "status": user.status.value
                }
            
            # In a real implementation, you would validate the token here
            # For now, we'll assume the token is valid if provided
            if not token:
                raise ValidationException("Invalid verification token")
            
            # Verify email
            user.verify_email()
            user.updated_at = datetime.utcnow()
            
            # Update user in repository
            updated_user = await self.user_repository.update(user)
            
            return {
                "message": "Email verified successfully",
                "user_id": updated_user.id,
                "status": updated_user.status.value,
                "email_verified": updated_user.email_verified
            }
            
        except (ValidationException, NotFoundException):
            raise
        except Exception as e:
            raise Exception(f"Email verification failed: {str(e)}")