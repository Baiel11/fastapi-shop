from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import require_admin, get_pagination_params
from ...services.customer.product_service import ProductService
from ...schemas.customer.product import ProductCreate, ProductResponse
from ...schemas.customer.pagination import PaginationParams, PaginatedResponse

router = APIRouter(prefix="/api/admin/products", tags=["admin"])


@router.get("", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    db: AsyncSession = Depends(get_db),
    params: PaginationParams = Depends(get_pagination_params),
    _=Depends(require_admin)
):
    """List all products including inactive ones (admin view)"""
    return await ProductService(db).get_all_products(params)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    return await ProductService(db).create_product(data)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    return await ProductService(db).update_product(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    """Soft-deletes the product (sets is_active=False)"""
    await ProductService(db).delete_product(product_id)
