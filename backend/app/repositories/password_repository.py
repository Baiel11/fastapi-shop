from datetime import datetime, timezone
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.password_reset_token import PasswordResetToken


class PasswordRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(self, user_id: int, token_hash: str, expires_at: datetime) -> PasswordResetToken:
        # Invalidate any earlier unused links: only the newest email works
        await self.invalidate_unused_for_user(user_id)

        token = PasswordResetToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token


    async def find_valid(self, token_hash: str) -> PasswordResetToken | None:
        """Return the row for a token that exists, is unused and unexpired."""
        now = datetime.now(timezone.utc)
        stmt = select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()


    async def mark_used(self, token_id: int) -> bool:
        """
        Atomically claim an unused, unexpired token for the caller.

        Like RefreshTokenRepository.revoke, the conditional UPDATE means only
        one caller can flip used_at from NULL — two concurrent submissions of
        the same link cannot both win.
        """
        stmt = (
            update(PasswordResetToken)
            .where(
                PasswordResetToken.id == token_id,
                PasswordResetToken.used_at.is_(None),
                PasswordResetToken.expires_at > datetime.now(timezone.utc),
            )
            .values(used_at=datetime.now(timezone.utc))
        )
        result = await self.db.execute(stmt)
        was_claimed = (result.rowcount or 0) > 0
        await self.db.commit()
        return was_claimed


    async def invalidate_unused_for_user(self, user_id: int) -> None:
        now = datetime.now(timezone.utc)
        stmt = (
            update(PasswordResetToken)
            .where(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.used_at.is_(None),
            )
            .values(used_at=now)
        )
        await self.db.execute(stmt)


    async def delete_expired(self) -> int:
        """Remove expired tokens. Returns the number of rows deleted."""
        now = datetime.now(timezone.utc)
        stmt = delete(PasswordResetToken).where(PasswordResetToken.expires_at < now)
        result = await self.db.execute(stmt)
        deleted = result.rowcount or 0
        await self.db.commit()
        return deleted
