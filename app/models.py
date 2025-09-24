from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    style_preference: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    mastery_records: Mapped[list["StudentMastery"]] = relationship(
        "StudentMastery", back_populates="student", cascade="all, delete-orphan"
    )
    goals: Mapped[list["StudentGoal"]] = relationship(
        "StudentGoal", back_populates="student", cascade="all, delete-orphan"
    )


class StudentMastery(Base):
    __tablename__ = "student_mastery"
    __table_args__ = (
        UniqueConstraint("student_id", "knowledge_point_id", name="uq_mastery_student_kp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    knowledge_point_id: Mapped[str] = mapped_column(String(128), index=True)
    mastery: Mapped[float] = mapped_column(Float, default=0.0)

    student: Mapped[Student] = relationship("Student", back_populates="mastery_records")


class StudentGoal(Base):
    __tablename__ = "student_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    target_kp: Mapped[str] = mapped_column(String(128), index=True)

    student: Mapped[Student] = relationship("Student", back_populates="goals")