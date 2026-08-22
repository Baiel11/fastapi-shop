from sqlalchemy.ext.asyncio import AsyncSession

from ...models.user import User  # ← needed for return type annotation
from ...repositories.user_repository import UserRepository
from ...schemas.customer.auth import UserRegister, UserLogin, UserResponse
from .session_service import SessionService
from ...core.security import verify_password, hash_password
from ...core.exceptions import ConflictException, UnauthorizedException, ForbiddenException


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.session_service = SessionService(db)


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


    async def login(self, data: UserLogin) -> tuple[str, str]:
        user = await self.user_repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException(detail="Invalid email or password")

        if not user.is_active:
            raise ForbiddenException(detail="Account is disabled")

        return await self.session_service.issue_token_pair(user.id)
