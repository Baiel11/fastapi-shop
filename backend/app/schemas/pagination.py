from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationParams(BaseModel):
    """Container for pagination offset and limit calculation"""
    page: int
    size: int

    @property
    def offset(self) -> int:
        """How many items to skip in the DB query"""
        return (self.page - 1) * self.size
    

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int = Field(..., description="Total number of items in the database")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")

    model_config = {"from_attributes": True}