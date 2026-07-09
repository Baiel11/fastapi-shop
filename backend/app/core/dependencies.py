from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.auth_service import AuthService
from ..core.exceptions import ForbiddenException

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