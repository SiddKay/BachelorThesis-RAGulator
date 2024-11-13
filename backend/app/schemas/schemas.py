from pydantic import BaseModel
from datetime import datetime
from typing import List


class AnswerBase(BaseModel):
    content: str


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    question_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    content: str


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    session_id: int
    created_at: datetime
    answers: List[Answer] = []

    class Config:
        from_attributes = True


class SessionBase(BaseModel):
    pass


class SessionCreate(SessionBase):
    pass


class Session(SessionBase):
    id: int
    created_at: datetime
    questions: List[Question] = []

    class Config:
        from_attributes = True
