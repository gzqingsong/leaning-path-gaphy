from __future__ import annotations
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
from app.repositories.graph_inmemory import InMemoryKnowledgeGraph
from app.services.path_planner import PathPlanner
from app.services.personalization import PersonalizationService

_engine = None
_SessionLocal: Optional[async_sessionmaker[AsyncSession]] = None
_graph: Optional[InMemoryKnowledgeGraph] = None
_planner: Optional[PathPlanner] = None
_personalizer: Optional[PersonalizationService] = None

class Base(DeclarativeBase):
    pass

def init_container() -> None:
    global _engine, _SessionLocal, _graph, _planner, _personalizer
    if _engine is None:
        _engine = create_async_engine(settings.database_url, echo=settings.debug)
        _SessionLocal = async_sessionmaker(bind=_engine, expire_on_commit=False)
    if _graph is None:
        _graph = InMemoryKnowledgeGraph()
    if _planner is None:
        _planner = PathPlanner(_graph)
    if _personalizer is None:
        _personalizer = PersonalizationService(_graph)

async def get_session() -> AsyncSession:
    assert _SessionLocal is not None
    async with _SessionLocal() as session:
        yield session

def get_graph() -> InMemoryKnowledgeGraph:
    assert _graph is not None
    return _graph

def get_planner() -> PathPlanner:
    assert _planner is not None
    return _planner

def get_personalizer() -> PersonalizationService:
    assert _personalizer is not None
    return _personalizer

async def init_db() -> None:
    # Import models to register metadata
    from app.db import models  # noqa: F401
    assert _engine is not None
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
