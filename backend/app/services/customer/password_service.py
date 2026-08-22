from datetime import datetime, timezone, timedelta
import hashlib
import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from ...repositories.user_repository import UserRepository
from ...repositories.password_repository import PasswordRepository
from ...repositories.refresh_token_repository import RefreshTokenRepository
from ...core.config import settings
from ...core.security import hash_password
from ...core.exceptions import UnauthorizedException


class PasswordService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.password_repo = PasswordRepository(db)
        self.refresh_token_repo = RefreshTokenRepository(db)


    async def request_password_reset(self, email: str) -> str | None:
        """
        Create a single-use reset token and return the frontend link.

        Returns None for unknown/inactive emails — callers MUST respond with
        an identical 204 either way so the endpoint can't be used to probe
        which addresses have accounts.
        """
        user = await self.user_repo.get_by_email(email)
        if not user or not user.is_active:
            return None

        # Raw token exists only in the email; DB keeps just its SHA-256 hash.
        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.reset_token_expire_minutes
        )
        await self.password_repo.create(user.id, token_hash, expires_at)

        return f"{settings.frontend_url}/reset-password?token={raw_token}"


    async def reset_password(self, raw_token: str, new_password: str) -> None:
        """Validate the single-use token, swap the password, kill all sessions."""
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        reset_row = await self.password_repo.find_valid(token_hash)
        if not reset_row:
            raise UnauthorizedException(detail="Invalid or expired reset link")

        user = await self.user_repo.get_by_id(reset_row.user_id)
        if not user or not user.is_active:
            raise UnauthorizedException(detail="Invalid or expired reset link")

        if not await self.password_repo.mark_used(reset_row.id):
            raise UnauthorizedException(detail="Invalid or expired reset link")

        await self.user_repo.update_password(user.id, hash_password(new_password))
        await self.refresh_token_repo.revoke_all_for_user(user.id)
        await self.password_repo.delete_expired()
