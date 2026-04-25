from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.product_service import ProductService
from ..schemas.product import ProductResponse, ProductListResponse

router = APIRouter(
    prefix="/api/products",
    tags=['products']
)

@router("", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()

@router("/{product_id}", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_id(product_id)

@router("/category/{category_id}", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_products_by_category(category_id)