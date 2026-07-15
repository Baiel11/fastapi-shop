from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..services.cart_service import CartService
from ..schemas.cart import(
    CartResponse, AddToCartRequest, UpdateCartRequest
)

router = APIRouter(
    prefix="/api/cart",
    tags=["cart"]
)

@router.get("", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    return await service.get_cart(current_user.id)

@router.post("/add", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def add_to_cart(request: AddToCartRequest, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    return await service.add_to_cart(current_user.id, request.product_id, request.quantity)

@router.put("/update", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def update_cart_item(request: UpdateCartRequest, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    return await service.update_cart_item(current_user.id, request.product_id, request.quantity)

@router.delete("/remove/{product_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def remove_from_cart(product_id: int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = CartService(db)
    return await service.remove_from_cart(current_user.id, product_id)