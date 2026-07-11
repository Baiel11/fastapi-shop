from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from decimal import Decimal

class CartItemBase(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, le=100, description="Quantity (quantity 0-100)")
    
class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, le=100, description="New quantity (quantity 0-100)")

class CartItem(BaseModel):
    product_id: int = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    price: Decimal = Field(..., description="Product price")
    quantity: int = Field(..., description="Quantity in cart")
    subtotal: Decimal = Field(..., description="Total price for this item (price * quantity)")
    image_url: Optional[str] = Field(None, description="Product image URL")

class CartResponse(BaseModel):
    items: List[CartItem] = Field(..., description="List of items in cart")
    total: Decimal = Field(..., description="Total cart price")
    items_count: int = Field(..., description="Total number of items in cart")

class AddToCartRequest(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID to add")
    quantity: int = Field(..., gt=0, le=100, description="Quantity to add (1-100)")
    cart: Dict[int, int] = Field(default_factory=dict)


class UpdateCartRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=100)
    cart: Dict[int, int] = Field(default_factory=dict)

class RemoveFromCartRequest(BaseModel):
    cart: Dict[int, int] = Field(default_factory=dict)