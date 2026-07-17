from sqlalchemy.ext.asyncio import AsyncSession
from ...repositories.user_repository import UserRepository
from ...schemas.admin.user_admin import AdminUserResponse
from ...schemas.customer.pagination import PaginationParams, PaginatedResponse
from ...core.exceptions import NotFoundException, BadRequestException


class UserAdminService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def get_all_users(self, params: PaginationParams) -> PaginatedResponse[AdminUserResponse]:
        total = await self.user_repo.count_all()
        users = await self.user_repo.get_all(offset=params.offset, limit=params.size)
        items = [AdminUserResponse.model_validate(u) for u in users]
        pages = (total + params.size - 1) // params.size if total > 0 else 1
        return PaginatedResponse[AdminUserResponse](
            items=items, total=total, page=params.page, size=params.size, pages=pages
        )

    async def set_user_active(self, user_id: int, is_active: bool) -> AdminUserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with id {user_id} not found")
        user.is_active = is_active
        await self.db.commit()
        await self.db.refresh(user)
        return AdminUserResponse.model_validate(user)

    async def set_admin_role(self, user_id: int, is_admin: bool, current_admin_id: int) -> AdminUserResponse:
        if user_id == current_admin_id:
            raise BadRequestException(detail="Cannot change your own admin role")
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with id {user_id} not found")
        user.is_admin = is_admin
        await self.db.commit()
        await self.db.refresh(user)
        return AdminUserResponse.model_validate(user)
