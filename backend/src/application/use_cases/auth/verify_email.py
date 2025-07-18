from datetime import datetime
from typing import Any

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
                user_id = verification_data["user_id"]
                token = verification_data["token"]

                # Get user
                user = await self.uow.users.get_by_id(user_id)
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

                # In a real implementation, you would validate the token here
                # For now, we'll assume the token is valid if provided
                if not token:
                    raise ValidationException("Invalid verification token")

                # Verify email
                user.verify_email()
                user.updated_at = datetime.utcnow()

                # Update user in repository
                updated_user = await self.uow.users.update(user)
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
