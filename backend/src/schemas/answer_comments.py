from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class AnswerCommentBase(BaseModel):
    """Base Pydantic model for AnswerComment"""

    comment_text: str


class AnswerCommentCreate(AnswerCommentBase):
    """Pydantic model for AnswerComment creation"""

    answer_id: UUID


class AnswerCommentRead(AnswerCommentBase):
    """Pydantic model for AnswerComment reading"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    answer_id: UUID
    created_at: datetime
