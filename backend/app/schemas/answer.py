from typing import Optional, List
from uuid import UUID
from pydantic import Field
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema
from app.schemas.answer_comment import AnswerComment


class AnswerBase(BaseSchema):
    chain_id: UUID
    question_id: UUID
    configuration_id: UUID
    generated_answer: str
    score: Optional[int] = Field(None, ge=0, le=5)


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase, TimeStampSchema, IdSchema):
    pass


class AnswerDetail(Answer):
    comments: List[AnswerComment] = []
