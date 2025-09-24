from __future__ import annotations
from typing import Optional, Dict, List
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON
from app.core.container import Base

class Student(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    knowledge_state: Mapped[Dict[str, float]] = mapped_column(JSON)
    goals: Mapped[List[str]] = mapped_column(JSON)
    style: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
