from .dashboard import router as dashboard_router
from .products import router as admin_products_router
from .categories import router as admin_categories_router
from .users import router as admin_users_router

__all__ = [
    "dashboard_router",
    "admin_products_router",
    "admin_categories_router",
    "admin_users_router",
]
