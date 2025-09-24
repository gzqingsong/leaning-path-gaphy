from typing import Dict, List
from sqlalchemy.orm import Session

from app.config import settings
from app.models import StudentMastery, StudentGoal
from app.services.planner import planner_service


class AdjustmentService:
    def adjust_and_replan(self, db: Session, student_id: int, kp_id: str, correct_rate: float, actual_time: float | None = None) -> Dict:
        # Update mastery with a simple EMA-like update
        mastery_record = db.query(StudentMastery).filter_by(student_id=student_id, knowledge_point_id=kp_id).one_or_none()
        new_mastery = max(0.0, min(1.0, correct_rate))
        if mastery_record is None:
            mastery_record = StudentMastery(student_id=student_id, knowledge_point_id=kp_id, mastery=new_mastery)
            db.add(mastery_record)
        else:
            mastery_record.mastery = (mastery_record.mastery * 0.5) + (new_mastery * 0.5)
        db.commit()

        # Build mastery map
        mastery_map = {
            rec.knowledge_point_id: rec.mastery
            for rec in db.query(StudentMastery).filter_by(student_id=student_id).all()
        }
        # Get current targets
        targets = [g.target_kp for g in db.query(StudentGoal).filter_by(student_id=student_id).all()]
        if not targets:
            return {"message": "no targets set"}
        paths = planner_service.plan(mastery_map, targets, mastery_threshold=settings.mastery_threshold_default)
        return {"paths": paths}


adjustment_service = AdjustmentService()