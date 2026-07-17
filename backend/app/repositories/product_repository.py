from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing import Optional
from ..models.product import Product
from ..schemas.customer.product import ProductCreate

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, offset: int, limit: int) -> list[Product]:
        """Fetch a sorted page of all products."""
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .order_by(Product.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.unique().scalars().all())
    
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def get_by_category(self, category_id: int, offset: int, limit: int) -> list[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.category_id == category_id)
            .order_by(Product.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.unique().scalars().all())
    
    async def create(self, product_data: ProductCreate) -> Product:
        db_product = Product(**product_data.model_dump())
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product
    
    async def get_multiple_by_ids(self, product_ids: list[int]) -> list[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id.in_(product_ids))
        )
        result = await self.db.execute(stmt)
        return list(result.unique().scalars().all())

    async def count_all(self) -> int:
        stmt = select(func.count(Product.id))
        result = await self.db.execute(stmt)
        return result.scalar() or 0
    
    async def count_by_category(self, category_id: int) -> int:
        stmt = select(func.count(Product.id)).where(Product.category_id == category_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0
    
    async def update(self, product_id: int, data) -> Optional[Product]:
        product = await self.get_by_id(product_id)
        if product:
            for key, value in data.model_dump().items():
                setattr(product, key, value)
            await self.db.commit()
            await self.db.refresh(product)
        return product

    async def soft_delete(self, product_id: int) -> bool:
        """Sets is_active=False"""
        product = await self.get_by_id(product_id)
        if product:
            product.is_active = False
            await self.db.commit()
            return True
        return False