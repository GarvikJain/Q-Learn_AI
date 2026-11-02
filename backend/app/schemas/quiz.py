from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any, Union
from uuid import UUID
import json


class QuestionResponse(BaseModel):
    id: UUID
    question_text: str
    question_type: str
    options: List[str]
    explanation: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator("options", mode="before")
    @classmethod
    def parse_options(cls, v: Any) -> List[str]:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(x) for x in parsed]
            except json.JSONDecodeError:
                return [v]
        return []


class QuizResponse(BaseModel):
    id: UUID
    module_id: UUID
    title: str
    questions: List[QuestionResponse]

    class Config:
        from_attributes = True


class QuizSubmit(BaseModel):
    answers: Dict[str, str]


class FeedbackItem(BaseModel):
    is_correct: bool
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None


class QuizResult(BaseModel):
    score: float
    max_score: float
    percentage: float
    feedback: Dict[str, FeedbackItem]
