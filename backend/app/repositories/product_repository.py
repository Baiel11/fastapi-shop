from sqlalchemy.orm import Session, joinedload
from typing import Optional
from ..models.product import Product
from ..schemas.product import ProductCreate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, offset: int, limit: int) -> list[Product]:
        """Fetch a sorted page of all products."""
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .order_by(Product.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_category(self, category_id: int, offset: int, limit: int) -> list[Product]:
        """Fetch a sorted page of products in a category."""
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.category_id == category_id)
            .order_by(Product.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def create(self, product_data: ProductCreate) -> Product:
        db_product = self.db(**product_data.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_multiple_by_ids(self, product_ids: list[int]) -> list[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id.in_(product_ids))
            .all()
        )

    def count_all(self) -> int:
        """Count total products in the database."""
        return self.db.query(Product).count()

    def count_by_category(self, category_id: int) -> int:
        """Count total products in a specific category."""
        return (
            self.db.query(Product)
            .filter(Product.category_id == category_id)
            .count()
        )