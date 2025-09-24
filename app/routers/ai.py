from fastapi import APIRouter
from app.schemas import EdgeIn
from app.services.llm import llm_service

router = APIRouter()

@router.post("/validate/prerequisite")
def validate_prerequisite(edge: EdgeIn):
    verdict = llm_service.validate_prereq(edge.prerequisite, edge.target)
    return {"verdict": verdict or "LLM not configured", "prerequisite": edge.prerequisite, "target": edge.target}