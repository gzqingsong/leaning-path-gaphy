from typing import Optional, List, Literal
from pydantic import BaseModel, Field


# Students
class StudentCreate(BaseModel):
    name: str
    style_preference: Optional[str] = None


class StudentRead(BaseModel):
    id: int
    name: str
    style_preference: Optional[str] = None

    class Config:
        from_attributes = True


class MasteryUpdate(BaseModel):
    knowledge_point_id: str
    mastery: float = Field(ge=0.0, le=1.0)


class GoalUpdate(BaseModel):
    targets: List[str]


# Graph
class NodeIn(BaseModel):
    id: str
    difficulty: float = 1.0
    importance: float = 1.0
    estimated_time: float = 1.0
    resource_types: List[str] = Field(default_factory=list)


class EdgeIn(BaseModel):
    prerequisite: str
    target: str


class NodeOut(BaseModel):
    id: str
    difficulty: float
    importance: float
    estimated_time: float
    resource_types: List[str]


# Planning
class PlanRequest(BaseModel):
    student_id: int
    targets: List[str]
    algorithm: Literal["dijkstra", "astar"] = "dijkstra"
    mastery_threshold: Optional[float] = None
    top_k: int = 1


class PlanPath(BaseModel):
    sequence: List[str]
    total_estimated_time: float
    total_difficulty: float
    score: float


class PlanResponse(BaseModel):
    paths: List[PlanPath]


# Feedback / Adjustment
class PerformanceFeedback(BaseModel):
    student_id: int
    knowledge_point_id: str
    correct_rate: float = Field(ge=0.0, le=1.0)
    actual_time: Optional[float] = None