from fastapi import Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.auth_service import AuthService
from ..core.exceptions import ForbiddenException
from ..schemas.pagination import PaginationParams

bearer_scheme = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db)
    ):
    token = credentials.credentials
    service = AuthService(db)
    return service.get_user_by_token(token)

def require_admin(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise ForbiddenException(detail="Admin access required")
    return current_user

async def get_pagination_params(
    page: int = Query(default=1, ge=1, description="Page number, starting from 1"),
    size: int = Query(default=20, ge=1, le=100, description="Items per page (max 100)")
) -> PaginationParams:
    """FastAPI Dependency to parse and validate pagination query parameters."""
    return PaginationParams(page=page, size=size)