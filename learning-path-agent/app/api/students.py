from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.container import get_session
from app.repositories.profile_repo import StudentProfileRepository
from app.models.domain import StudentProfile

router = APIRouter(prefix="/students", tags=["students"])
repo = StudentProfileRepository()

@router.get("/", response_model=list[StudentProfile])
async def list_students(session: AsyncSession = Depends(get_session)):
    return await repo.list(session)

@router.get("/{student_id}", response_model=StudentProfile)
async def get_student(student_id: str, session: AsyncSession = Depends(get_session)):
    res = await repo.get(session, student_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return res

@router.put("/{student_id}", response_model=StudentProfile)
async def upsert_student(student_id: str, profile: StudentProfile, session: AsyncSession = Depends(get_session)):
    if student_id != profile.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    return await repo.upsert(session, profile)

@router.delete("/{student_id}")
async def delete_student(student_id: str, session: AsyncSession = Depends(get_session)):
    await repo.delete(session, student_id)
    return {"deleted": True}
