from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.entities.verification_token import TokenType, VerificationToken
from ....core.repositories.verification_token_repository import (
    VerificationTokenRepository,
)
from ..models.verification_token_model import VerificationTokenModel

if TYPE_CHECKING:
    # Type checking only imports to avoid circular imports
    pass


class VerificationTokenRepositoryImpl(VerificationTokenRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, token: VerificationToken) -> VerificationToken:
        """Create a new verification token"""
        db_token = VerificationTokenModel(
            user_id=token.user_id,
            token=token.token,
            token_type=token.token_type
            if isinstance(token.token_type, str)
            else token.token_type.value,
            expires_at=token.expires_at,
            used=token.used,
            created_at=token.created_at,
        )

        self.db.add(db_token)
        await self.db.commit()
        await self.db.refresh(db_token)

        return self._to_entity(db_token)

    async def get_by_token(self, token: str) -> VerificationToken | None:
        """Get verification token by token string"""
        result = await self.db.execute(
            select(VerificationTokenModel).where(VerificationTokenModel.token == token)
        )
        db_token = result.scalar_one_or_none()
        return self._to_entity(db_token) if db_token else None

    async def get_valid_token(
        self, user_id: int, token_type: TokenType
    ) -> VerificationToken | None:
        """Get valid (not expired, not used) token for user and type"""
        now = datetime.utcnow()
        result = await self.db.execute(
            select(VerificationTokenModel)
            .where(
                and_(
                    VerificationTokenModel.user_id == user_id,
                    VerificationTokenModel.token_type == token_type
                    if isinstance(token_type, str)
                    else token_type.value,
                    not VerificationTokenModel.used,
                    VerificationTokenModel.expires_at > now,
                )
            )
            .order_by(VerificationTokenModel.created_at.desc())
        )
        db_token = result.scalar_one_or_none()
        return self._to_entity(db_token) if db_token else None

    async def update(self, token: VerificationToken) -> VerificationToken:
        """Update verification token"""
        result = await self.db.execute(
            select(VerificationTokenModel).where(VerificationTokenModel.id == token.id)
        )
        db_token = result.scalar_one_or_none()

        if not db_token:
            raise ValueError("Token not found")

        db_token.used = token.used
        db_token.expires_at = token.expires_at

        await self.db.commit()
        await self.db.refresh(db_token)

        return self._to_entity(db_token)

    async def delete_expired_tokens(self) -> int:
        """Delete all expired tokens and return count"""
        now = datetime.utcnow()
        result = await self.db.execute(
            select(VerificationTokenModel).where(
                VerificationTokenModel.expires_at <= now
            )
        )
        expired_tokens = result.scalars().all()

        for token in expired_tokens:
            await self.db.delete(token)  # type: ignore[arg-type]

        await self.db.commit()
        return len(expired_tokens)

    async def invalidate_user_tokens(self, user_id: int, token_type: TokenType) -> int:
        """Invalidate all tokens for a user of a specific type"""
        result = await self.db.execute(
            select(VerificationTokenModel).where(
                and_(
                    VerificationTokenModel.user_id == user_id,
                    VerificationTokenModel.token_type == token_type
                    if isinstance(token_type, str)
                    else token_type.value,
                    not VerificationTokenModel.used,
                )
            )
        )
        tokens = result.scalars().all()

        for token in tokens:
            token.used = True

        await self.db.commit()
        return len(tokens)

    def _to_entity(self, db_token: VerificationTokenModel) -> VerificationToken:
        """Convert database model to domain entity"""
        return VerificationToken(
            id=db_token.id,  # type: ignore[arg-type]
            user_id=db_token.user_id,  # type: ignore[arg-type]
            token=db_token.token,  # type: ignore[arg-type]
            token_type=TokenType(db_token.token_type),  # type: ignore[arg-type]
            expires_at=db_token.expires_at,  # type: ignore[arg-type]
            used=db_token.used,  # type: ignore[arg-type]
            created_at=db_token.created_at,  # type: ignore[arg-type]
        )
