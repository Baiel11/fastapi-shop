from fastapi import APIRouter, Depends, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...core.limiter import limiter
from ...core.security import set_refresh_cookie, clear_refresh_cookie, extract_refresh_token
from ...services.customer.auth_service import AuthService
from ...models.user import User
from ...schemas.customer.auth import UserRegister, UserLogin, TokenResponse, UserResponse, RefreshRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def register(request: Request, data: UserRegister, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register(data)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, response: Response, data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    access_token, refresh_token = await service.login(data)
    set_refresh_cookie(response, refresh_token)
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")
async def refresh(request: Request, response: Response, data: RefreshRequest | None = None, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    refresh_token = extract_refresh_token(request, data)
    access_token, new_refresh_token = await service.refresh(refresh_token)
    set_refresh_cookie(response, new_refresh_token)
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def logout(
    request: Request,
    response: Response,
    data: RefreshRequest | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AuthService(db)
    refresh_token = extract_refresh_token(request, data)
    await service.logout(refresh_token, current_user)
    clear_refresh_cookie(response)


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def logout_all(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AuthService(db)
    await service.logout_all(current_user)
    # This session's refresh token was revoked server-side as well.
    clear_refresh_cookie(response)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
