from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import json
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.module import Module
from app.models.quiz import Quiz, Question, QuizAttempt
from app.models.progress import UserProgress
from app.schemas.quiz import QuizResponse, QuizSubmit, QuizResult

router = APIRouter()

@router.get("/{module_slug}", response_model=QuizResponse)
async def get_quiz(module_slug: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).filter(Module.slug == module_slug))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    result = await db.execute(select(Quiz).filter(Quiz.module_id == module.id))
    quiz = result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    result = await db.execute(select(Question).filter(Question.quiz_id == quiz.id))
    questions = result.scalars().all()
    
    quiz_dict = {
        "id": quiz.id,
        "module_id": quiz.module_id,
        "title": quiz.title,
        "questions": questions
    }
    return quiz_dict

@router.post("/{module_slug}/submit", response_model=QuizResult)
async def submit_quiz(module_slug: str, submit: QuizSubmit, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).filter(Module.slug == module_slug))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    result = await db.execute(select(Quiz).filter(Quiz.module_id == module.id))
    quiz = result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    result = await db.execute(select(Question).filter(Question.quiz_id == quiz.id))
    questions = result.scalars().all()
    
    score = 0.0
    max_score = len(questions)
    feedback = {}

    for q in questions:
        ans = submit.answers.get(str(q.id))
        is_correct = ans == q.correct_answer
        feedback[str(q.id)] = {
            "is_correct": is_correct,
            "correct_answer": None if is_correct else q.correct_answer,
            "explanation": q.explanation,
        }
        if is_correct:
            score += 1.0

    percentage = (score / max_score) * 100 if max_score > 0 else 0

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=score,
        answers_json=json.dumps(submit.answers),
    )
    db.add(attempt)

    result = await db.execute(
        select(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.module_id == module.id,
        )
    )
    progress = result.scalars().first()
    if progress:
        progress.quiz_attempts += 1
        progress.quiz_score = max(progress.quiz_score or 0.0, score)
        progress.status = "completed"
    else:
        progress = UserProgress(
            user_id=current_user.id,
            module_id=module.id,
            quiz_attempts=1,
            quiz_score=score,
            status="completed",
        )
        db.add(progress)

    await db.commit()

    return QuizResult(
        score=score,
        max_score=max_score,
        percentage=percentage,
        feedback=feedback,
    )
