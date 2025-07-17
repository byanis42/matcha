from typing import Dict, Any
from datetime import datetime
import secrets

from ....core.entities.user import User
from ....core.value_objects.email import Email
from ....core.repositories.user_repository import UserRepository
from ....shared.exceptions import ValidationException, NotFoundException
from ....shared.security import hash_password


class ResetPasswordUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def request_reset(self, email: str) -> Dict[str, Any]:
        """
        Request password reset - send reset token
        """
        try:
            # Validate email
            email_obj = Email(email)
            
            # Get user by email
            user = await self.user_repository.get_by_email(str(email_obj))
            if not user:
                # Don't reveal if email exists or not for security
                return {
                    "message": "If the email exists, a reset link has been sent",
                    "email": email
                }
            
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            
            # In a real implementation, you would:
            # 1. Store the reset token with expiration in database
            # 2. Send email with reset link
            
            return {
                "message": "Password reset email sent",
                "email": email,
                "reset_token": reset_token  # Remove in production
            }
            
        except Exception as e:
            raise Exception(f"Password reset request failed: {str(e)}")

    async def confirm_reset(self, reset_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Confirm password reset with token and new password
        """
        try:
            email = reset_data["email"]
            token = reset_data["token"]
            new_password = reset_data["new_password"]
            
            # Validate email
            email_obj = Email(email)
            
            # Get user by email
            user = await self.user_repository.get_by_email(str(email_obj))
            if not user:
                raise NotFoundException("User not found")
            
            # In a real implementation, you would validate the reset token here
            # For now, we'll assume the token is valid if provided
            if not token:
                raise ValidationException("Invalid reset token")
            
            # Hash new password
            new_password_hash = hash_password(new_password)
            
            # Update user password
            user.password_hash = new_password_hash
            user.updated_at = datetime.utcnow()
            
            # Update user in repository
            updated_user = await self.user_repository.update(user)
            
            return {
                "message": "Password reset successfully",
                "user_id": updated_user.id,
                "email": str(updated_user.email)
            }
            
        except (ValidationException, NotFoundException):
            raise
        except Exception as e:
            raise Exception(f"Password reset failed: {str(e)}")