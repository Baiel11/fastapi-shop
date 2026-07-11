from pydantic import BaseModel, Field, field_validator
import re

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Category name"
    ) # actually placeholder
    slug: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="URL-friendly category name"
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip()
    
    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str) -> str:
        value = value.lower().strip()
        if not SLUG_PATTERN.fullmatch(value):
            raise ValueError("Slug must be lowercase words seperated by single hyphens")
        return value
    
class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int = Field(..., description='Unique category identifier')
    
    model_config = {"from_attributes": True}