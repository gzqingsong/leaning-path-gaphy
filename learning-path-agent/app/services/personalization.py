from __future__ import annotations
from typing import List
from app.models.domain import PlannedPath
from app.repositories.graph_inmemory import InMemoryKnowledgeGraph

class PersonalizationService:
    def __init__(self, graph: InMemoryKnowledgeGraph) -> None:
        self.graph = graph

    def recommend_resources(self, path: PlannedPath, style: str | None) -> List[dict]:
        recommendations = []
        for step in path.steps:
            node = self.graph.node_attr(step.node_id)
            tags = node.get("resource_tags", [])
            preferred = None
            if style == "visual":
                preferred = [t for t in tags if t in ("video", "diagram", "slides")]
            elif style == "auditory":
                preferred = [t for t in tags if t in ("podcast", "audio", "lecture")]
            else:
                preferred = tags
            recommendations.append({"node_id": step.node_id, "resources": preferred})
        return recommendations

    def balance_cognitive_load(self, path: PlannedPath) -> PlannedPath:
        adjusted = []
        high_count = 0
        for step in path.steps:
            diff = self.graph.node_attr(step.node_id).get("difficulty", 0)
            if diff >= 0.7:
                high_count += 1
            else:
                high_count = 0
            adjusted.append(step)
        return path
