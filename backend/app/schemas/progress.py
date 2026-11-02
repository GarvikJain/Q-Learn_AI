from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProgressResponse(BaseModel):
    module_id: UUID
    status: str
    quiz_score: Optional[float] = None
    quiz_attempts: int = 0
    time_spent_minutes: int = 0
    last_accessed: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    status: Optional[str] = None
    time_spent_minutes: Optional[int] = None
