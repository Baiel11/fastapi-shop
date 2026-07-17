from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_products: int
    active_products: int
    total_categories: int
