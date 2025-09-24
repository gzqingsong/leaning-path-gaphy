from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Student, StudentMastery, StudentGoal
from app.schemas import StudentCreate, StudentRead, MasteryUpdate, GoalUpdate

router = APIRouter()


@router.post("/", response_model=StudentRead)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    s = Student(name=payload.name, style_preference=payload.style_preference)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/", response_model=List[StudentRead])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    s = db.get(Student, student_id)
    if not s:
        raise HTTPException(status_code=404, detail="Student not found")
    return s


@router.post("/{student_id}/mastery")
def update_mastery(student_id: int, updates: List[MasteryUpdate], db: Session = Depends(get_db)):
    if not db.get(Student, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    for u in updates:
        rec = db.query(StudentMastery).filter_by(student_id=student_id, knowledge_point_id=u.knowledge_point_id).one_or_none()
        if rec is None:
            rec = StudentMastery(student_id=student_id, knowledge_point_id=u.knowledge_point_id, mastery=u.mastery)
            db.add(rec)
        else:
            rec.mastery = u.mastery
    db.commit()
    return {"updated": len(updates)}


@router.post("/{student_id}/goals")
def set_goals(student_id: int, payload: GoalUpdate, db: Session = Depends(get_db)):
    if not db.get(Student, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    db.query(StudentGoal).filter_by(student_id=student_id).delete()
    for kp in payload.targets:
        db.add(StudentGoal(student_id=student_id, target_kp=kp))
    db.commit()
    return {"targets": payload.targets}