import secrets
from datetime import datetime
from typing import Any

from ....core.repositories.unit_of_work import AbstractUnitOfWork
from ....core.value_objects.email import Email
from ....shared.exceptions import NotFoundException, ValidationException
from ....shared.security import hash_password


class ResetPasswordUseCase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def request_reset(self, email: str) -> dict[str, Any]:
        """
        Request password reset - send reset token
        """
        try:
            # Validate email
            email_obj = Email(email)

            # Get user by email
            user = await self.uow.users.get_by_email(str(email_obj))
            if not user:
                # Don't reveal if email exists or not for security
                return {
                    "message": "If the email exists, a reset link has been sent",
                    "email": email,
                }

            # Generate reset token
            reset_token = secrets.token_urlsafe(32)

            # In a real implementation, you would:
            # 1. Store the reset token with expiration in database
            # 2. Send email with reset link

            return {
                "message": "Password reset email sent",
                "email": email,
                "reset_token": reset_token,  # Remove in production
            }

        except Exception as e:
            raise Exception(f"Password reset request failed: {str(e)}") from e

    async def confirm_reset(self, reset_data: dict[str, Any]) -> dict[str, Any]:
        """
        Confirm password reset with token and new password
        """
        try:
            async with self.uow:
                email = reset_data["email"]
                token = reset_data["token"]
                new_password = reset_data["new_password"]

                # Validate email
                email_obj = Email(email)

                # Get user by email
                user = await self.uow.users.get_by_email(str(email_obj))
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
                updated_user = await self.uow.users.update(user)
                await self.uow.commit()

                return {
                    "message": "Password reset successfully",
                    "user_id": updated_user.id,
                    "email": str(updated_user.email),
                }

        except (ValidationException, NotFoundException):
            raise
        except Exception as e:
            raise Exception(f"Password reset failed: {str(e)}") from e
