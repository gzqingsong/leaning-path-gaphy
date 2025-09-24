from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Student
from app.graph.store import store

router = APIRouter()


@router.get("/{student_id}/recommendations")
def recommend_resources(student_id: int, targets: List[str] | None = None, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    style = (student.style_preference or "").lower()

    nodes = store.list_nodes()
    if targets:
        targets_set = set(targets)
        nodes = [n for n in nodes if n["id"] in targets_set]

    def score(node):
        rtypes = [rt.lower() for rt in node.get("resource_types", [])]
        preferred = 1 if style and style in rtypes else 0
        importance = float(node.get("importance", 1.0))
        return (preferred * 2.0) + importance

    ranked = sorted(nodes, key=score, reverse=True)
    # Return top 10 lightweight recommendation descriptions
    return [
        {
            "knowledge_point_id": n["id"],
            "suggested_types": n.get("resource_types", []),
            "reason": f"match:{style in [rt.lower() for rt in n.get('resource_types', [])]} importance:{n.get('importance', 1.0)}",
        }
        for n in ranked[:10]
    ]