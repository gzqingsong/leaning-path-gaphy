## Learning Path Planner API

### Quickstart

- Build and run with Docker:
```bash
docker compose up --build
```
- Seed sample graph (in another terminal):
```bash
docker compose exec api python scripts/seed.py
```
- Health check: `GET http://localhost:8000/health`
- Plan path: `POST http://localhost:8000/api/plan/` with body:
```json
{
  "id": "s1",
  "name": "Alice",
  "knowledge_state": {"A": 0.9},
  "goals": ["C"],
  "style": "visual"
}
```

### Endpoints
- `POST /api/graph/load` load knowledge graph
- `GET /api/graph/prereqs/{node_id}` query prerequisites
- `POST /api/plan/` plan with `algo` = `dijkstra` or `a*`
- `POST /api/personalize/resources` recommend resources
- `POST /api/personalize/balance` balance cognitive load
- `POST /api/adjust/` dynamic adjustment with performance/time_ratio
- `GET/PUT/DELETE /api/students/...` student profiles

### Tech
- FastAPI, Pydantic v2, NetworkX, SQLAlchemy Async (SQLite), optional Neo4j
