from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID


class QuestionBase(BaseModel):
    """Base Pydantic model for Question"""

    question_text: str
    expected_answer: Optional[str] = None
    sequence_number: int


class QuestionCreate(QuestionBase):
    """Pydantic model for Question creation"""

    session_id: UUID


class QuestionRead(QuestionBase):
    """Pydantic model for Question reading"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    session_id: UUID
