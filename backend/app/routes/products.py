from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_pagination_params
from ..services.product_service import ProductService
from ..schemas.product import ProductResponse
from ..schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(
    prefix="/api/products",
    tags=['products']
)

@router.get("", response_model=PaginatedResponse[ProductResponse], status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db), pagination: PaginationParams = Depends(get_pagination_params)):
    service = ProductService(db)
    return service.get_all_products(pagination)

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_id(product_id)

@router.get("/category/{category_id}", response_model=PaginatedResponse[ProductResponse], status_code=status.HTTP_200_OK)
def get_products_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination_params)
):
    service = ProductService(db)
    return service.get_products_by_category(category_id, pagination)