from typing import Dict, List, Tuple, Optional, Iterable, Set
import networkx as nx

NodeAttrs = Dict[str, object]


class GraphStore:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    # Nodes
    def upsert_node(self, node_id: str, attrs: Optional[NodeAttrs] = None) -> None:
        if attrs is None:
            attrs = {}
        self.graph.add_node(node_id, **attrs)

    def get_node(self, node_id: str) -> Optional[NodeAttrs]:
        if node_id in self.graph:
            data = self.graph.nodes[node_id]
            return {"id": node_id, **dict(data)}
        return None

    def list_nodes(self) -> List[NodeAttrs]:
        return [{"id": n, **dict(d)} for n, d in self.graph.nodes(data=True)]

    def delete_node(self, node_id: str) -> None:
        if node_id in self.graph:
            self.graph.remove_node(node_id)

    # Edges (prerequisite -> target)
    def add_edge(self, prerequisite: str, target: str) -> None:
        self.graph.add_edge(prerequisite, target)

    def remove_edge(self, prerequisite: str, target: str) -> None:
        if self.graph.has_edge(prerequisite, target):
            self.graph.remove_edge(prerequisite, target)

    def list_edges(self) -> List[Tuple[str, str]]:
        return list(self.graph.edges())

    # Utilities
    def get_prerequisites_closure(self, targets: Iterable[str]) -> Set[str]:
        required: Set[str] = set()
        for t in targets:
            if t not in self.graph:
                continue
            ancestors = nx.ancestors(self.graph, t)
            required.update(ancestors)
            required.add(t)
        return required

    def topological_order(self, nodes_subset: Iterable[str]) -> List[str]:
        sub = self.graph.subgraph(nodes_subset).copy()
        if not nx.is_directed_acyclic_graph(sub):
            # Attempt to break cycles conservatively by removing back-edges (not ideal)
            try:
                cycle = next(nx.simple_cycles(sub))
                # remove one edge from cycle
                if len(cycle) > 1:
                    self.graph.remove_edge(cycle[-1], cycle[0])
                    sub = self.graph.subgraph(nodes_subset).copy()
            except StopIteration:
                pass
        return list(nx.topological_sort(sub))

    def get_attrs(self, node_id: str) -> NodeAttrs:
        data = self.graph.nodes.get(node_id, {})
        return dict(data)


# Singleton store
store = GraphStore()