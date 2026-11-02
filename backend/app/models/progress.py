from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"), nullable=False)
    status = Column(String, default="not_started")
    quiz_score = Column(Float, nullable=True)
    quiz_attempts = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
