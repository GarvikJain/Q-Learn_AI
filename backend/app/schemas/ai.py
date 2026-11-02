from pydantic import BaseModel
from typing import Optional, List

class AIRequest(BaseModel):
    question: str
    context: Optional[str] = None
    mode: str = 'beginner'

class AIResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    mode: str
