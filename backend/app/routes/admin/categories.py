from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import require_admin
from ...services.customer.category_service import CategoryService
from ...schemas.customer.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/api/admin/categories", tags=["admin"])


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    return await CategoryService(db).create_category(data)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    return await CategoryService(db).update_category(category_id, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    await CategoryService(db).delete_category(category_id)
