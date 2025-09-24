from typing import List
from fastapi import APIRouter, HTTPException

from app.graph.store import store
from app.schemas import NodeIn, NodeOut, EdgeIn

router = APIRouter()


@router.get("/nodes", response_model=List[NodeOut])
def list_nodes():
    return store.list_nodes()


@router.post("/nodes", response_model=NodeOut)
def upsert_node(node: NodeIn):
    store.upsert_node(node.id, {
        "difficulty": node.difficulty,
        "importance": node.importance,
        "estimated_time": node.estimated_time,
        "resource_types": node.resource_types,
    })
    n = store.get_node(node.id)
    if not n:
        raise HTTPException(status_code=500, detail="Failed to upsert node")
    return n


@router.delete("/nodes/{node_id}")
def delete_node(node_id: str):
    store.delete_node(node_id)
    return {"deleted": node_id}


@router.get("/edges")
def list_edges():
    return [{"prerequisite": u, "target": v} for u, v in store.list_edges()]


@router.post("/edges")
def add_edge(edge: EdgeIn):
    store.add_edge(edge.prerequisite, edge.target)
    return {"added": True}


@router.delete("/edges")
def remove_edge(edge: EdgeIn):
    store.remove_edge(edge.prerequisite, edge.target)
    return {"removed": True}