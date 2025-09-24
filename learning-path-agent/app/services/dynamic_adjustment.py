from __future__ import annotations
from typing import Dict
from app.models.domain import PlannedPath

class DynamicAdjustmentService:
    def adjust(self, path: PlannedPath, performance: Dict[str, float], time_ratio: Dict[str, float]) -> PlannedPath:
        for step in path.steps:
            acc = performance.get(step.node_id)
            t = time_ratio.get(step.node_id)
            reasons = []
            if acc is not None and acc < 0.5:
                reasons.append("low-accuracy")
            if t is not None and t > 1.5:
                reasons.append("slow-progress")
            if t is not None and t < 0.5:
                reasons.append("fast-progress")
            if reasons:
                step.reason = ",".join(reasons)
        return path
