from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.limiter import limiter
from ...infrastructure.email import send_password_reset_email
from ...services.customer.password_service import PasswordService
from ...schemas.customer.auth import ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter(prefix="/api/auth", tags=["password"])


@router.post("/forgot-password", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("3/minute")
async def forgot_password(
    request: Request,
    background_tasks: BackgroundTasks,
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    service = PasswordService(db)
    reset_link = await service.request_password_reset(data.email)

    if reset_link:
        background_tasks.add_task(send_password_reset_email, data.email, reset_link)


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    service = PasswordService(db)
    await service.reset_password(data.token, data.password)
