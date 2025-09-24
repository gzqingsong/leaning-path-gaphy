from fastapi import APIRouter
from app.core.container import get_planner
from app.services.dynamic_adjustment import DynamicAdjustmentService
from app.models.domain import PlannedPath

router = APIRouter(prefix="/adjust", tags=["adjust"])

_service = DynamicAdjustmentService()

@router.post("/")
async def adjust_path(path: PlannedPath, performance: dict[str, float] = {}, time_ratio: dict[str, float] = {}):
    return _service.adjust(path, performance, time_ratio)
