import asyncio
from app.core.container import init_container, init_db, get_graph
from app.models.domain import KnowledgeNode, KnowledgeEdge

SAMPLE_NODES = [
    KnowledgeNode(id="A", name="Basics", difficulty=0.2, importance=0.8, estimated_time_min=30, resource_tags=["video","slides"]),
    KnowledgeNode(id="B", name="Intermediate", difficulty=0.5, importance=0.9, estimated_time_min=45, resource_tags=["article","exercise"]),
    KnowledgeNode(id="C", name="Advanced", difficulty=0.8, importance=1.0, estimated_time_min=60, resource_tags=["video","exercise"]),
]

SAMPLE_EDGES = [
    KnowledgeEdge(source="A", target="B", relation="prerequisite"),
    KnowledgeEdge(source="B", target="C", relation="prerequisite"),
]

async def main():
    init_container()
    await init_db()
    graph = get_graph()
    graph.load(SAMPLE_NODES, SAMPLE_EDGES)
    print("Seeded graph with", len(SAMPLE_NODES), "nodes and", len(SAMPLE_EDGES), "edges")

if __name__ == "__main__":
    asyncio.run(main())
