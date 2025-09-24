from __future__ import annotations
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class KnowledgeNode(BaseModel):
    id: str = Field(..., description="Unique identifier of the knowledge point")
    name: str
    difficulty: float = Field(ge=0.0, le=1.0)
    importance: float = Field(ge=0.0, le=1.0)
    estimated_time_min: int = Field(ge=1)
    resource_tags: List[str] = []

class KnowledgeEdge(BaseModel):
    source: str
    target: str
    relation: str  # prerequisite, part_of, related

class StudentProfile(BaseModel):
    id: str
    name: str
    knowledge_state: Dict[str, float]  # node_id -> mastery [0,1]
    goals: List[str]
    style: Optional[str] = None  # visual, auditory, etc.

class PathStep(BaseModel):
    node_id: str
    reason: Optional[str] = None

class PlannedPath(BaseModel):
    steps: List[PathStep]
    total_estimated_time_min: int
    total_difficulty: float
    score: float
