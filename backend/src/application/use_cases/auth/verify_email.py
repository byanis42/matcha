from datetime import datetime
from typing import Any

from ....core.entities.verification_token import TokenType
from ....core.repositories.unit_of_work import AbstractUnitOfWork
from ....shared.exceptions import NotFoundException, ValidationException


class VerifyEmailUseCase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, verification_data: dict[str, Any]) -> dict[str, Any]:
        """
        Verify user email with token
        """
        try:
            async with self.uow:
                token_str = verification_data["token"]

                # Get verification token
                verification_token = await self.uow.verification_tokens.get_by_token(token_str)
                if not verification_token:
                    raise ValidationException("Invalid verification token")

                # Check if token is valid
                if not verification_token.is_valid():
                    if verification_token.is_expired():
                        raise ValidationException("Verification token has expired")
                    else:
                        raise ValidationException("Verification token has already been used")

                # Check if it's an email verification token
                if verification_token.token_type != TokenType.EMAIL_VERIFICATION:
                    raise ValidationException("Invalid token type")

                # Get user
                user = await self.uow.users.get_by_id(verification_token.user_id)
                if not user:
                    raise NotFoundException("User not found")

                # Check if already verified
                if user.email_verified:
                    return {
                        "message": "Email already verified",
                        "user_id": user.id,
                        "status": user.status,
                        "email_verified": True,
                    }

                # Verify email
                user.verify_email()
                user.updated_at = datetime.utcnow()

                # Mark token as used
                verification_token.use_token()

                # Update user and token in repository
                updated_user = await self.uow.users.update(user)
                await self.uow.verification_tokens.update(verification_token)
                await self.uow.commit()

                return {
                    "message": "Email verified successfully",
                    "user_id": updated_user.id,
                    "status": updated_user.status,
                    "email_verified": updated_user.email_verified,
                }

        except (ValidationException, NotFoundException):
            raise
        except Exception as e:
            raise Exception(f"Email verification failed: {str(e)}") from e
