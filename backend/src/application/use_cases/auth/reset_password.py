import secrets
from datetime import datetime, timedelta
from typing import Any

from ....core.entities.verification_token import TokenType, VerificationToken
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
            async with self.uow:
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
                expires_at = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiration

                # Store reset token in database
                verification_token = VerificationToken(
                    user_id=user.id,
                    token=reset_token,
                    token_type=TokenType.PASSWORD_RESET,
                    expires_at=expires_at,
                    created_at=datetime.utcnow()
                )
                await self.uow.verification_tokens.create(verification_token)

                # Send password reset email
                await self.uow.email_service.send_password_reset_email(
                    email=str(user.email),
                    username=user.username,
                    token=reset_token
                )
                
                await self.uow.commit()

                return {
                    "message": "Password reset email sent",
                    "email": email,
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

                # Get and validate reset token
                verification_token = await self.uow.verification_tokens.get_by_token(token)
                if not verification_token:
                    raise ValidationException("Invalid reset token")

                # Check if token is valid
                if not verification_token.is_valid():
                    if verification_token.is_expired():
                        raise ValidationException("Reset token has expired")
                    else:
                        raise ValidationException("Reset token has already been used")

                # Check if it's a password reset token
                if verification_token.token_type != TokenType.PASSWORD_RESET:
                    raise ValidationException("Invalid token type")

                # Check if token belongs to the user
                if verification_token.user_id != user.id:
                    raise ValidationException("Token does not belong to this user")

                # Hash new password
                new_password_hash = hash_password(new_password)

                # Update user password
                user.password_hash = new_password_hash
                user.updated_at = datetime.utcnow()

                # Mark token as used
                verification_token.used = True
                await self.uow.verification_tokens.update(verification_token)

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
