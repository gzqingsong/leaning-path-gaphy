from fastapi import APIRouter
from app.api.plan import router as plan_router
from app.api.students import router as students_router
from app.api.graph import router as graph_router
from app.api.adjust import router as adjust_router
from app.api.personalize import router as personalize_router

router = APIRouter()

router.include_router(plan_router)
router.include_router(students_router)
router.include_router(graph_router)
router.include_router(adjust_router)
router.include_router(personalize_router)
