from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import require_admin, get_pagination_params
from ...services.admin.user_admin_service import UserAdminService
from ...schemas.admin.user_admin import AdminUserResponse, UpdateUserStatus, UpdateUserRole
from ...schemas.customer.pagination import PaginationParams, PaginatedResponse

router = APIRouter(prefix="/api/admin/users", tags=["admin"])


@router.get("", response_model=PaginatedResponse[AdminUserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    params: PaginationParams = Depends(get_pagination_params),
    _=Depends(require_admin)
):
    return await UserAdminService(db).get_all_users(params)


@router.patch("/{user_id}/status", response_model=AdminUserResponse)
async def set_user_status(
    user_id: int,
    data: UpdateUserStatus,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    """Ban or unban a user (sets is_active)"""
    return await UserAdminService(db).set_user_active(user_id, data.is_active)


@router.patch("/{user_id}/role", response_model=AdminUserResponse)
async def set_user_role(
    user_id: int,
    data: UpdateUserRole,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    """Promote or demote a user's admin status. Cannot change own role"""
    return await UserAdminService(db).set_admin_role(user_id, data.is_admin, current_admin.id)
