from fastapi import APIRouter
from app.api.plan import router as plan_router
from app.api.students import router as students_router
from app.api.graph import router as graph_router

router = APIRouter()

router.include_router(plan_router)
router.include_router(students_router)
router.include_router(graph_router)
