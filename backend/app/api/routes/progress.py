from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, get_current_instructor
from app.models.user import User
from app.models.module import Module
from app.models.progress import UserProgress
from app.schemas.progress import ProgressResponse, ProgressUpdate
import datetime

router = APIRouter()


@router.get("", response_model=List[ProgressResponse])
async def get_all_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UserProgress).filter(UserProgress.user_id == current_user.id)
    )
    return result.scalars().all()


@router.get("/summary")
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Module))
    total_modules = len(result.scalars().all())

    result = await db.execute(
        select(UserProgress).filter(UserProgress.user_id == current_user.id)
    )
    progress_list = result.scalars().all()

    completed = sum(1 for p in progress_list if p.status == "completed")
    in_progress = sum(1 for p in progress_list if p.status == "in_progress")
    total_time = sum(p.time_spent_minutes for p in progress_list)
    scores = [p.quiz_score for p in progress_list if p.quiz_score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0

    return {
        "total_modules": total_modules,
        "completed": completed,
        "in_progress": in_progress,
        "avg_quiz_score": round(avg_score, 1),
        "total_time_minutes": total_time,
    }


@router.get("/instructor/learners")
async def get_learners(
    current_user: User = Depends(get_current_instructor),
    db: AsyncSession = Depends(get_db),
):
    """Return real learner analytics from the database."""
    result = await db.execute(select(func.count()).select_from(Module))
    total_modules = result.scalar() or 0

    result = await db.execute(select(User).filter(User.role == "student"))
    students = result.scalars().all()

    learners = []
    struggling = 0
    completion_rates = []

    for student in students:
        result = await db.execute(
            select(UserProgress).filter(UserProgress.user_id == student.id)
        )
        rows = result.scalars().all()
        completed = sum(1 for p in rows if p.status == "completed")
        in_progress = sum(1 for p in rows if p.status == "in_progress")
        scores = [p.quiz_score for p in rows if p.quiz_score is not None]
        avg_score = round(sum(scores) / len(scores), 1) if scores else None
        completion_pct = (
            round((completed / total_modules) * 100, 1) if total_modules else 0
        )
        completion_rates.append(completion_pct)
        if avg_score is not None and avg_score < 2.0 and completed > 0:
            struggling += 1
        learners.append(
            {
                "user_id": str(student.id),
                "username": student.username,
                "email": student.email,
                "completed_modules": completed,
                "in_progress_modules": in_progress,
                "avg_quiz_score": avg_score,
                "completion_pct": completion_pct,
            }
        )

    avg_completion = (
        round(sum(completion_rates) / len(completion_rates), 1)
        if completion_rates
        else 0
    )

    return {
        "total_learners": len(students),
        "avg_completion_pct": avg_completion,
        "struggling_learners": struggling,
        "learners": learners,
    }


@router.put("/{module_slug}", response_model=ProgressResponse)
async def update_progress(
    module_slug: str,
    update: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Module).filter(Module.slug == module_slug))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    result = await db.execute(
        select(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.module_id == module.id,
        )
    )
    progress = result.scalars().first()

    if not progress:
        progress = UserProgress(user_id=current_user.id, module_id=module.id)
        db.add(progress)

    if update.status:
        progress.status = update.status
    if update.time_spent_minutes is not None:
        progress.time_spent_minutes += update.time_spent_minutes

    progress.last_accessed = datetime.datetime.utcnow()
    await db.commit()
    await db.refresh(progress)
    return progress
