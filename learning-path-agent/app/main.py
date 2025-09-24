from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as plan_router
from app.api.students import router as students_router
from app.api.graph import router as graph_router
from app.core.container import init_container, init_db

app = FastAPI(title="Learning Path Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    init_container()
    await init_db()

app.include_router(plan_router, prefix="/api")
app.include_router(students_router, prefix="/api")
app.include_router(graph_router, prefix="/api")
