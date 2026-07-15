from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from typing import List, Optional
from ..models.cart_item import CartItem

class CartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_and_product(self, user_id: int, product_id: int) -> Optional[CartItem]:
        stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def get_user_cart(self, user_id: int) -> List[CartItem]:
        stmt = (
            select(CartItem)
            .options(joinedload(CartItem.product))
            .where(CartItem.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return list(result.unique().scalars().all())
    
    async def add_or_update_item(self, user_id: int, product_id: int, quantity: int) -> CartItem:
        db_cart_item = await self.get_by_user_and_product(user_id, product_id)
        if db_cart_item:
            db_cart_item.quantity += quantity
        else:
            db_cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            self.db.add(db_cart_item)
        await self.db.commit()
        await self.db.refresh(db_cart_item)
        return db_cart_item
    
    async def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> Optional[CartItem]:
        db_cart_item = await self.get_by_user_and_product(user_id, product_id)
        if db_cart_item:
            db_cart_item.quantity = quantity
            await self.db.commit()
            await self.db.refresh(db_cart_item)
        return db_cart_item
    
    async def remove_item(self, user_id: int, product_id: int) -> bool:
        db_cart_item = await self.get_by_user_and_product(user_id, product_id)
        if db_cart_item:
            await self.db.delete(db_cart_item)
            await self.db.commit()
            return True
        return False
    
    async def clear_cart(self, user_id: int) -> None:
        stmt = delete(CartItem).where(CartItem.user_id == user_id)
        await self.db.execute(stmt)
        await self.db.commit()