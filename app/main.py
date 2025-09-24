from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.health import router as health_router
from app.routers.graph import router as graph_router
from app.routers.students import router as students_router
from app.routers.planning import router as planning_router
from app.routers.resources import router as resources_router
from app.routers.adjustment import router as adjustment_router
from app.db import engine
from app.models import Base

app = FastAPI(title="Learning Path Planning Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["health"]) 
app.include_router(graph_router, prefix="/graph", tags=["graph"]) 
app.include_router(students_router, prefix="/students", tags=["students"]) 
app.include_router(planning_router, prefix="/planning", tags=["planning"]) 
app.include_router(resources_router, prefix="/resources", tags=["resources"]) 
app.include_router(adjustment_router, prefix="/adjustment", tags=["adjustment"]) 

@app.get("/")
def root():
    return {"service": app.title, "version": app.version, "env": settings.environment}


@app.on_event("startup")
def on_startup():
    # Create DB tables
    Base.metadata.create_all(bind=engine)