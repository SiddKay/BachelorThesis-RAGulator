from datetime import datetime
from typing import List, Optional
from uuid import UUID
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema
from app.schemas.answer import AnswerDetail


class QuestionBase(BaseSchema):
    question_text: str
    expected_answer: Optional[str] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionBulkCreate(BaseSchema):
    questions: List[QuestionCreate]


class QuestionUpdate(BaseSchema):
    question_text: Optional[str] = None
    expected_answer: Optional[str] = None


class Question(QuestionBase, TimeStampSchema, IdSchema):
    last_modified: datetime


class QuestionBulkDelete(BaseSchema):
    question_ids: List[UUID]


class QuestionDetail(Question):
    answers: List[AnswerDetail] = []
