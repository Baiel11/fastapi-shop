from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from ...services.customer.category_service import CategoryService
from ...schemas.customer.category import CategoryResponse

router = APIRouter(
    prefix="/api/categories",
    tags=['categories']
)

@router.get("", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_categories(db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_all_categories()

@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_category_by_id(category_id)