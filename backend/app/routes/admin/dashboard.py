from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import require_admin
from ...services.admin.dashboard_service import DashboardService
from ...schemas.admin.dashboard import DashboardStats

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    return await DashboardService(db).get_stats()
