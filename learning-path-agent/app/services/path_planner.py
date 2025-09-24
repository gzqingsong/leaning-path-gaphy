from __future__ import annotations
from typing import List, Dict, Tuple, Optional, Set
import heapq
from app.models.domain import StudentProfile, PlannedPath, PathStep
from app.repositories.graph_inmemory import InMemoryKnowledgeGraph

class PathPlanner:
    def __init__(self, graph: InMemoryKnowledgeGraph) -> None:
        self.graph = graph

    def _cost(self, node_id: str) -> float:
        attr = self.graph.node_attr(node_id)
        return attr.get("estimated_time_min", 1) * (1 + attr.get("difficulty", 1))

    def _heuristic(self, node_id: str, goals: Set[str]) -> float:
        # Simple heuristic: distance to any goal by edge count
        return 0.0 if node_id in goals else 1.0

    def _prereqs_met(self, node_id: str, mastered: Set[str]) -> bool:
        for pre in self.graph.get_prerequisites(node_id):
            if pre not in mastered:
                return False
        return True

    def _score(self, path: List[str], profile: StudentProfile) -> float:
        total_time = sum(self.graph.node_attr(n).get("estimated_time_min", 1) for n in path)
        total_diff = sum(self.graph.node_attr(n).get("difficulty", 1.0) for n in path)
        weak_nodes = [n for n in path if profile.knowledge_state.get(n, 0.0) < 0.5]
        return 1.0 / (1 + total_time + total_diff * 10) + len(weak_nodes) * 0.001

    def plan_dijkstra(self, profile: StudentProfile) -> PlannedPath:
        mastered = {n for n, m in profile.knowledge_state.items() if m >= 0.8}
        goals = set(profile.goals)
        frontier: List[Tuple[float, List[str]]] = []

        for node_id in list(self.graph.graph.nodes):
            if node_id in mastered:
                continue
            if self._prereqs_met(node_id, mastered):
                heapq.heappush(frontier, (self._cost(node_id), [node_id]))

        best_path: Optional[List[str]] = None
        best_cost = float("inf")
        visited: Set[Tuple[str, ...]] = set()

        while frontier:
            cost, path = heapq.heappop(frontier)
            if tuple(path) in visited:
                continue
            visited.add(tuple(path))

            if goals.issubset(set(path) | mastered):
                best_path = path
                best_cost = cost
                break

            last = path[-1]
            for nb in self.graph.neighbors(last):
                if nb in mastered or nb in path:
                    continue
                if not self._prereqs_met(nb, mastered | set(path)):
                    continue
                new_cost = cost + self._cost(nb)
                if new_cost < best_cost:
                    heapq.heappush(frontier, (new_cost, path + [nb]))

        steps = [PathStep(node_id=n) for n in (best_path or [])]
        return PlannedPath(
            steps=steps,
            total_estimated_time_min=sum(self.graph.node_attr(n).get("estimated_time_min", 1) for n in (best_path or [])),
            total_difficulty=sum(self.graph.node_attr(n).get("difficulty", 1.0) for n in (best_path or [])),
            score=self._score(best_path or [], profile),
        )

    def plan_a_star(self, profile: StudentProfile) -> PlannedPath:
        mastered = {n for n, m in profile.knowledge_state.items() if m >= 0.8}
        goals = set(profile.goals)
        frontier: List[Tuple[float, List[str]]] = []

        for node_id in list(self.graph.graph.nodes):
            if node_id in mastered:
                continue
            if self._prereqs_met(node_id, mastered):
                g = self._cost(node_id)
                f = g + self._heuristic(node_id, goals)
                heapq.heappush(frontier, (f, [node_id]))

        best_path: Optional[List[str]] = None
        best_f = float("inf")
        visited: Set[Tuple[str, ...]] = set()

        while frontier:
            f, path = heapq.heappop(frontier)
            if tuple(path) in visited:
                continue
            visited.add(tuple(path))

            if goals.issubset(set(path) | mastered):
                best_path = path
                best_f = f
                break

            last = path[-1]
            for nb in self.graph.neighbors(last):
                if nb in mastered or nb in path:
                    continue
                if not self._prereqs_met(nb, mastered | set(path)):
                    continue
                g = sum(self._cost(n) for n in path) + self._cost(nb)
                new_f = g + self._heuristic(nb, goals)
                if new_f < best_f:
                    heapq.heappush(frontier, (new_f, path + [nb]))

        steps = [PathStep(node_id=n) for n in (best_path or [])]
        return PlannedPath(
            steps=steps,
            total_estimated_time_min=sum(self.graph.node_attr(n).get("estimated_time_min", 1) for n in (best_path or [])),
            total_difficulty=sum(self.graph.node_attr(n).get("difficulty", 1.0) for n in (best_path or [])),
            score=self._score(best_path or [], profile),
        )
