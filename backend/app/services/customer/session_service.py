from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from ...models.user import User
from ...repositories.user_repository import UserRepository
from ...repositories.refresh_token_repository import RefreshTokenRepository
from ...core.security import create_access_token, create_refresh_token, decode_token
from ...core.exceptions import UnauthorizedException


class SessionService:
    """Owns the token lifecycle: issuing pairs, rotation, revocation,
    and resolving users from access tokens."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.refresh_token_repo = RefreshTokenRepository(db)


    async def issue_token_pair(self, user_id: int) -> tuple[str, str]:
        payload = {"sub": str(user_id)}
        refresh_token = create_refresh_token(payload)
        refresh_payload = decode_token(refresh_token)

        await self.refresh_token_repo.create(
            user_id=user_id,
            jti=refresh_payload["jti"],
            expires_at=datetime.fromtimestamp(refresh_payload["exp"], tz=timezone.utc),
        )

        await self.refresh_token_repo.delete_expired()

        return create_access_token(payload), refresh_token


    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        try:
            payload = decode_token(refresh_token)
            token_type: str = payload.get("type")
            jti: str = payload.get("jti")
            user_id = payload.get("sub")

            if token_type != "refresh" or jti is None or user_id is None:
                raise UnauthorizedException(detail="Invalid refresh token")
            user_id = int(user_id)
        except (JWTError, ValueError):
            raise UnauthorizedException(detail="Invalid or expired refresh token")

        if not await self.refresh_token_repo.revoke(jti):
            raise UnauthorizedException(detail="Refresh token has been revoked or expired")

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException(detail="User not found or blocked")

        return await self.issue_token_pair(user.id)


    async def logout(self, refresh_token: str, user: User) -> None:
        try:
            payload = decode_token(refresh_token)
            jti: str = payload.get("jti")
            token_user_id = payload.get("sub")

            if payload.get("type") != "refresh" or jti is None:
                raise UnauthorizedException(detail="Invalid refresh token")
            if token_user_id is None or int(token_user_id) != user.id:
                raise UnauthorizedException(detail="Refresh token does not belong to this user")
        except (JWTError, ValueError):
            raise UnauthorizedException(detail="Invalid or expired refresh token")

        await self.refresh_token_repo.revoke(jti)


    async def logout_all(self, user: User) -> None:
        """Invalidate every active session for the given user."""
        await self.refresh_token_repo.revoke_all_for_user(user.id)


    async def get_user_by_token(self, token: str) -> User:
        try:
            payload = decode_token(token)
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")

            if user_id is None or token_type != "access":
                raise UnauthorizedException(detail="Invalid token")

            user_id = int(user_id)

        except (JWTError, ValueError):
            raise UnauthorizedException(detail="Invalid or expired token")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException(detail="User not found")

        if not user.is_active:
            raise UnauthorizedException(detail="User is blocked")

        return user
