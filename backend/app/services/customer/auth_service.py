from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from ...models.user import User  # ← needed for return type annotation
from ...repositories.user_repository import UserRepository
from ...repositories.refresh_token_repository import RefreshTokenRepository
from ...schemas.customer.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from ...core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)
from ...core.exceptions import ConflictException, UnauthorizedException, ForbiddenException


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.refresh_token_repo = RefreshTokenRepository(db)


    async def register(self, data: UserRegister) -> UserResponse:
        if await self.user_repo.get_by_email(data.email):
            raise ConflictException(detail="Email already registered")
        
        if await self.user_repo.get_by_username(data.username):
            raise ConflictException(detail="Username already taken")
        
        # Hash happens here
        hashed = hash_password(data.password)
        user = await self.user_repo.create(
            email=data.email,
            username=data.username,
            hashed_password=hashed
        )

        return UserResponse.model_validate(user)

    
    async def login(self, data: UserLogin) -> TokenResponse:
        user = await self.user_repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException(detail="Invalid email or password")
        
        if not user.is_active:
            raise ForbiddenException(detail="Account is disabled")
        
        return await self._issue_token_pair(user.id)


    async def refresh(self, refresh_token: str) -> TokenResponse:
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

        # Rotation is atomic: this call claims the old token (or loses the
        # race to a concurrent/replayed request and is rejected). The token
        # is consumed before any further work, so it can never be reused.
        if not await self.refresh_token_repo.revoke(jti):
            raise UnauthorizedException(detail="Refresh token has been revoked or expired")

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException(detail="User not found or blocked")

        return await self._issue_token_pair(user.id)


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


    async def _issue_token_pair(self, user_id: int) -> TokenResponse:
        payload = {"sub": str(user_id)}
        refresh_token = create_refresh_token(payload)
        refresh_payload = decode_token(refresh_token)

        await self.refresh_token_repo.create(
            user_id=user_id,
            jti=refresh_payload["jti"],
            expires_at=datetime.fromtimestamp(refresh_payload["exp"], tz=timezone.utc),
        )

        # Opportunistic housekeeping: run on the cheap, rate-limited auth
        # paths so expired rows don't accumulate without a background job.
        await self.refresh_token_repo.delete_expired()

        return TokenResponse(
            access_token=create_access_token(payload),
            refresh_token=refresh_token,
        )

    
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
