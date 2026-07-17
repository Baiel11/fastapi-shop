from decimal import DecimalException
from pydantic import BaseModel, Field, field_validator, HttpUrl
from datetime import datetime
from decimal import Decimal
from typing import Optional
from .category import CategoryResponse

class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Product name"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Product description"
    )
    price: Decimal = Field(
        ...,
        gt=0,
        lt=1_000_000,
        max_digits=10,
        decimal_places=2,
        description="Product price (price 0-1,000,000)"
    )
    category_id: int = Field(..., description='Category ID')
    image_url: Optional[HttpUrl] = Field(None, description='Product image URL')

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Product name cannot be blank")
        return value
    
    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            return value.strip()
        return value
    
    @field_validator("price", mode="before")
    @classmethod
    def validate_price(cls, value: str | float | int) -> Decimal:
        decimal_price = Decimal(str(value))
        if decimal_price.as_tuple().exponent < -2:
            raise ValueError("Price cannot have more than 2 decimal plces")
        return decimal_price
    
class ProductCreate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int = Field(..., description="Unique product ID")
    name: str
    description: Optional[str]
    price: Decimal
    category_id: int
    image_url: Optional[HttpUrl]
    created_at: datetime
    category: CategoryResponse = Field(..., description="Product category details")
    
    model_config = {"from_attributes": True}

class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int = Field(..., description='Total number of products')