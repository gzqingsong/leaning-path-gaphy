from fastapi import APIRouter, Depends
from app.core.container import get_planner, get_personalizer
from app.models.domain import StudentProfile, PlannedPath

router = APIRouter(prefix="/plan", tags=["plan"])

@router.post("/", response_model=PlannedPath)
async def plan_path(profile: StudentProfile, algo: str = "dijkstra"):
    planner = get_planner()
    if algo == "a*":
        planned = planner.plan_a_star(profile)
    else:
        planned = planner.plan_dijkstra(profile)
    return planned
