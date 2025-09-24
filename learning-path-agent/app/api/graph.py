from fastapi import APIRouter
from app.core.container import get_graph
from app.models.domain import KnowledgeNode, KnowledgeEdge

router = APIRouter(prefix="/graph", tags=["graph"])

@router.post("/load")
async def load_graph(nodes: list[KnowledgeNode], edges: list[KnowledgeEdge]):
    graph = get_graph()
    graph.load(nodes, edges)
    return {"nodes": len(nodes), "edges": len(edges)}

@router.get("/prereqs/{node_id}")
async def prereqs(node_id: str):
    graph = get_graph()
    return {"node_id": node_id, "prerequisites": graph.get_prerequisites(node_id)}
