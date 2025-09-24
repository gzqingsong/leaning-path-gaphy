import networkx as nx
from typing import Iterable, List, Dict
from app.models.domain import KnowledgeNode, KnowledgeEdge

class InMemoryKnowledgeGraph:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def load(self, nodes: Iterable[KnowledgeNode], edges: Iterable[KnowledgeEdge]) -> None:
        for n in nodes:
            self.graph.add_node(n.id, **n.model_dump())
        for e in edges:
            self.graph.add_edge(e.source, e.target, relation=e.relation)

    def get_prerequisites(self, node_id: str) -> List[str]:
        return [u for u, v, d in self.graph.in_edges(node_id, data=True) if d.get("relation") == "prerequisite"]

    def neighbors(self, node_id: str) -> List[str]:
        return list(self.graph.successors(node_id))

    def has_node(self, node_id: str) -> bool:
        return self.graph.has_node(node_id)

    def node_attr(self, node_id: str) -> Dict:
        return self.graph.nodes[node_id]
