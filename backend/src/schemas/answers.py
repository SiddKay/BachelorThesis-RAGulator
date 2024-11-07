from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID
from ..db.models import ScoreRange


class AnswerBase(BaseModel):
    """Base Pydantic model for Answer"""

    generated_text: str
    score: Optional[ScoreRange] = None


class AnswerCreate(AnswerBase):
    """Pydantic model for Answer creation"""

    evaluation_id: UUID
    question_id: UUID
    config_id: UUID


class AnswerRead(AnswerBase):
    """Pydantic model for Answer reading"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    evaluation_id: UUID
    question_id: UUID
    config_id: UUID
    generated_at: datetime
