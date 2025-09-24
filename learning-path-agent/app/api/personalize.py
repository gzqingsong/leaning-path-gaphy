from fastapi import APIRouter, Depends
from app.core.container import get_personalizer
from app.models.domain import PlannedPath

router = APIRouter(prefix="/personalize", tags=["personalize"])

@router.post("/resources")
async def recommend_resources(path: PlannedPath, style: str | None = None):
    service = get_personalizer()
    return service.recommend_resources(path, style)

@router.post("/balance", response_model=PlannedPath)
async def balance_load(path: PlannedPath):
    service = get_personalizer()
    return service.balance_cognitive_load(path)
