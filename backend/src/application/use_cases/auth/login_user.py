from typing import Any

from ....core.entities.user import UserStatus
from ....core.repositories.unit_of_work import AbstractUnitOfWork
from ....shared.exceptions import AuthenticationException
from ....shared.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)


class LoginUserUseCase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, login_data: dict[str, Any]) -> dict[str, Any]:
        """
        Authenticate user and return tokens
        """
        try:
            async with self.uow:
                # Get user by email or username
                user = None
                if "@" in login_data["identifier"]:
                    # Login with email
                    user = await self.uow.users.get_by_email(login_data["identifier"])
                else:
                    # Login with username
                    user = await self.uow.users.get_by_username(
                        login_data["identifier"]
                    )

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
                await self.uow.users.update(user)
                await self.uow.commit()

            # Generate tokens
            access_token = create_access_token(
                {"user_id": user.id, "email": str(user.email)}
            )
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
                    "status": user.status,
                    "email_verified": user.email_verified,
                    "last_seen": user.last_seen,
                    "created_at": user.created_at,
                },
            }

        except AuthenticationException:
            raise
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}") from e
