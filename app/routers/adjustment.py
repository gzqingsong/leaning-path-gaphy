from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Student
from app.schemas import PerformanceFeedback
from app.services.adjustment import adjustment_service

router = APIRouter()


@router.post("/")
def adjust(payload: PerformanceFeedback, db: Session = Depends(get_db)):
    student = db.get(Student, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return adjustment_service.adjust_and_replan(db, payload.student_id, payload.knowledge_point_id, payload.correct_rate, payload.actual_time)