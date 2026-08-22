from fastapi import Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from ..services.customer.session_service import SessionService
from ..models.user import User
from .exceptions import ForbiddenException
from ..schemas.customer.pagination import PaginationParams


bearer_scheme = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: AsyncSession = Depends(get_db)
    ) -> User:
    token = credentials.credentials
    service = SessionService(db)
    return await service.get_user_by_token(token)


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise ForbiddenException(detail="Admin access required")
    return current_user


async def get_pagination_params(
    page: int = Query(default=1, ge=1, description="Page number, starting from 1"),
    size: int = Query(default=20, ge=1, le=100, description="Items per page (max 100)")
) -> PaginationParams:
    """FastAPI Dependency to parse and validate pagination query parameters."""
    return PaginationParams(page=page, size=size)