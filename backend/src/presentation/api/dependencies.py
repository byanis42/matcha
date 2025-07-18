from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.repositories.unit_of_work import AbstractUnitOfWork
from ...core.repositories.user_repository import UserRepository
from ...infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl,
)
from ...infrastructure.database.session import get_db
from ...infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from ...shared.exceptions import AuthenticationException
from ...shared.security import get_current_user_from_token

security = HTTPBearer()


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Dependency to get user repository"""
    return UserRepositoryImpl(db)


async def get_uow(db: AsyncSession = Depends(get_db)) -> AbstractUnitOfWork:
    """Dependency to get Unit of Work"""
    return SqlAlchemyUnitOfWork(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> dict[str, Any]:
    """Dependency to get current authenticated user"""
    try:
        token = credentials.credentials
        user_data = get_current_user_from_token(token)

        # Verify user exists and is active
        async with uow:
            user = await uow.users.get_by_id(user_data["user_id"])
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
                )

            if not user.is_active():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User account is inactive",
                )

            return {
                "user_id": user.id,
                "username": user.username,
                "email": str(user.email),
                "status": user.status,
            }

    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from None


async def get_current_active_user(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Dependency to get current active user"""
    if current_user["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is not active",
        )
    return current_user
