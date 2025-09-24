from __future__ import annotations
from typing import Dict, List, Set, Iterable, Tuple

from app.config import settings
from app.graph.store import store
from app.services.llm import llm_service


class PlannerService:
    def __init__(self) -> None:
        pass

    def plan(self, mastered: Dict[str, float], targets: List[str], mastery_threshold: float | None = None, algorithm: str = "dijkstra", top_k: int = 1) -> List[Dict]:
        threshold = mastery_threshold or settings.mastery_threshold_default
        mastered_set = {kp for kp, m in mastered.items() if m >= threshold}

        required_set = store.get_prerequisites_closure(targets)
        learn_set = [kp for kp in required_set if kp not in mastered_set]
        if not learn_set:
            return [self._build_path([], 0.0, 0.0)]

        sequence = self._heuristic_topo_order(learn_set)
        total_time = sum(float(store.get_attrs(kp).get("estimated_time", 1.0)) for kp in sequence)
        total_difficulty = sum(float(store.get_attrs(kp).get("difficulty", 1.0)) for kp in sequence)
        score = self._score(sequence, total_time, total_difficulty, mastered)
        explanation = llm_service.explain_plan(sequence, context=f"targets={targets}")
        return [self._build_path(sequence, total_time, total_difficulty, score, explanation)]

    def _heuristic_topo_order(self, nodes: Iterable[str]) -> List[str]:
        # Kahn's algorithm with tie-breaking by lower (difficulty * estimated_time) and higher importance
        sub_nodes = set(nodes)
        subgraph = store.graph.subgraph(sub_nodes).copy()
        in_degree: Dict[str, int] = {n: subgraph.in_degree(n) for n in subgraph.nodes}
        ready = [n for n, d in in_degree.items() if d == 0]

        def node_cost(n: str) -> Tuple[float, float]:
            attrs = store.get_attrs(n)
            difficulty = float(attrs.get("difficulty", 1.0))
            time_cost = float(attrs.get("estimated_time", 1.0))
            importance = float(attrs.get("importance", 1.0))
            return (difficulty * time_cost, -importance)

        order: List[str] = []
        while ready:
            ready.sort(key=node_cost)
            n = ready.pop(0)
            order.append(n)
            for _u, v in list(subgraph.out_edges(n)):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    ready.append(v)
            subgraph.remove_node(n)
        return order

    def _score(self, sequence: List[str], total_time: float, total_difficulty: float, mastered: Dict[str, float]) -> float:
        # Lower is better: weighted sum of time and difficulty, plus emphasis on weak areas
        weakness_penalty = 0.0
        for kp in sequence:
            m = mastered.get(kp, 0.0)
            weakness_penalty += (1.0 - m)
        return total_time * 0.6 + total_difficulty * 0.3 + weakness_penalty * 0.1

    def _build_path(self, sequence: List[str], total_time: float, total_difficulty: float, score: float | None = None, explanation: str | None = None) -> Dict:
        if score is None:
            score = total_time * 0.6 + total_difficulty * 0.4
        return {
            "sequence": sequence,
            "total_estimated_time": total_time,
            "total_difficulty": total_difficulty,
            "score": float(score),
            "explanation": explanation,
        }


planner_service = PlannerService()