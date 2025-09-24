from __future__ import annotations
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models import Student
from app.models.domain import StudentProfile

class StudentProfileRepository:
    async def upsert(self, session: AsyncSession, profile: StudentProfile) -> StudentProfile:
        existing = await session.get(Student, profile.id)
        if existing is None:
            student = Student(
                id=profile.id,
                name=profile.name,
                knowledge_state=profile.knowledge_state,
                goals=profile.goals,
                style=profile.style,
            )
            session.add(student)
        else:
            existing.name = profile.name
            existing.knowledge_state = profile.knowledge_state
            existing.goals = profile.goals
            existing.style = profile.style
        await session.commit()
        row = await session.get(Student, profile.id)
        return StudentProfile(
            id=row.id,
            name=row.name,
            knowledge_state=row.knowledge_state,
            goals=row.goals,
            style=row.style,
        )

    async def get(self, session: AsyncSession, student_id: str) -> Optional[StudentProfile]:
        row = await session.get(Student, student_id)
        if row is None:
            return None
        return StudentProfile(
            id=row.id,
            name=row.name,
            knowledge_state=row.knowledge_state,
            goals=row.goals,
            style=row.style,
        )

    async def list(self, session: AsyncSession) -> List[StudentProfile]:
        result = await session.execute(select(Student))
        rows = result.scalars().all()
        return [
            StudentProfile(
                id=r.id,
                name=r.name,
                knowledge_state=r.knowledge_state,
                goals=r.goals,
                style=r.style,
            )
            for r in rows
        ]

    async def delete(self, session: AsyncSession, student_id: str) -> bool:
        await session.execute(delete(Student).where(Student.id == student_id))
        await session.commit()
        return True
