from typing import Optional, List
from uuid import UUID
from pydantic import Field
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema
from app.schemas.answer_comment import AnswerComment


class AnswerBase(BaseSchema):
    question_id: UUID
    chain_id: UUID
    configuration_id: UUID
    generated_answer: str
    score: Optional[int] = Field(None, ge=0, le=5)


class AnswerCreate(AnswerBase):
    pass


class AnswerBulkCreate(BaseSchema):
    answers: List[AnswerCreate]


class Answer(AnswerBase, TimeStampSchema, IdSchema):
    pass


class AnswerUpdate(BaseSchema):
    score: Optional[int] = Field(None, ge=0, le=5)


class AnswerDetail(Answer):
    comments: List[AnswerComment] = []
