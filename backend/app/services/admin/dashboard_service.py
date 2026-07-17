from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ...repositories.product_repository import ProductRepository
from ...repositories.user_repository import UserRepository
from ...repositories.category_repository import CategoryRepository
from ...models.product import Product
from ...models.user import User
from ...schemas.admin.dashboard import DashboardStats


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.user_repo = UserRepository(db)
        self.category_repo = CategoryRepository(db)

    async def get_stats(self) -> DashboardStats:
        total_users = await self.user_repo.count_all()

        active_users_result = await self.db.execute(
            select(func.count(User.id)).where(User.is_active == True)
        )
        active_users = active_users_result.scalar() or 0

        total_products = await self.product_repo.count_all()

        active_products_result = await self.db.execute(
            select(func.count(Product.id)).where(Product.is_active == True)
        )
        active_products = active_products_result.scalar() or 0

        from ...models.category import Category
        cat_result = await self.db.execute(select(func.count(Category.id)))
        total_categories = cat_result.scalar() or 0

        return DashboardStats(
            total_users=total_users,
            active_users=active_users,
            total_products=total_products,
            active_products=active_products,
            total_categories=total_categories,
        )
