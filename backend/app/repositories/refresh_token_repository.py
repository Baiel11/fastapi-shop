from datetime import datetime, timezone
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(self, user_id: int, jti: str, expires_at: datetime) -> RefreshToken:
        token = RefreshToken(user_id=user_id, jti=jti, expires_at=expires_at)
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token


    async def revoke(self, jti: str) -> bool:
        """
        Atomically claim an unrevoked, unexpired token for the caller.

        Only one caller can flip `revoked` to True for a given jti, so a
        rotation/reuse attempt that loses the race is rejected outright.
        Returns True when *this* call updated the row, False when the token
        was already revoked, already expired, or simply does not exist.
        """
        now = datetime.now(timezone.utc)
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.jti == jti,
                RefreshToken.revoked.is_(False),
                RefreshToken.expires_at > now,
            )
            .values(revoked=True)
        )
        result = await self.db.execute(stmt)
        was_revoked = (result.rowcount or 0) > 0
        await self.db.commit()
        return was_revoked


    async def revoke_all_for_user(self, user_id: int) -> None:
        stmt = update(RefreshToken).where(RefreshToken.user_id == user_id).values(revoked=True)
        await self.db.execute(stmt)
        await self.db.commit()


    async def delete_expired(self) -> int:
        """Remove expired tokens. Returns the number of rows deleted."""
        now = datetime.now(timezone.utc)
        stmt = delete(RefreshToken).where(RefreshToken.expires_at < now)
        result = await self.db.execute(stmt)
        deleted = result.rowcount or 0
        await self.db.commit()
        return deleted
