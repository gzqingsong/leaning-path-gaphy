from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Student, StudentMastery
from app.schemas import PlanRequest, PlanResponse, PlanPath
from app.services.planner import planner_service

router = APIRouter()


@router.post("/plan", response_model=PlanResponse)
def plan(payload: PlanRequest, db: Session = Depends(get_db)):
    student = db.get(Student, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    mastery_map: Dict[str, float] = {
        r.knowledge_point_id: r.mastery for r in db.query(StudentMastery).filter_by(student_id=payload.student_id).all()
    }
    paths_dict = planner_service.plan(mastery_map, payload.targets, mastery_threshold=payload.mastery_threshold, algorithm=payload.algorithm, top_k=payload.top_k)
    paths = [PlanPath(**p) for p in paths_dict]
    return PlanResponse(paths=paths)