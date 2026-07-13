from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.cart_item import CartItem

class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_and_product(self, user_id: int, product_id: int) -> Optional[CartItem]:
        return (
            self.db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
            .first()
        )
    
    def get_user_cart(self, user_id: int) -> List[CartItem]:
        return (
            self.db.query(CartItem)
            .options(joinedload(CartItem.product))
            .filter(CartItem.user_id == user_id)
            .all()
        )
    
    def add_or_update_item(self, user_id: int, product_id: int, quantity: int) -> CartItem:
        db_cart_item = self.get_by_user_and_product(user_id, product_id)
        if db_cart_item:
            db_cart_item.quantity += quantity
        else:
            db_cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            self.db.add(db_cart_item)
        self.db.commit()
        self.db.refresh(db_cart_item)
        return db_cart_item
    
    def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> Optional[CartItem]:
        db_cart_item = self.get_by_user_and_product(user_id, product_id)
        if db_cart_item:
            db_cart_item.quantity = quantity
            self.db.commit()
            self.db.refresh(db_cart_item)
        return db_cart_item
    
    def remove_item(self, user_id: int, product_id: int) -> bool:
        db_cart_item = self.get_by_user_and_product(user_id, product_id)
        if db_cart_item:
            self.db.delete(db_cart_item)
            self.db.commit()
            return True
        return False
    
    def clear_cart(self, user_id: int) -> None:
        self.db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        self.db.commit()