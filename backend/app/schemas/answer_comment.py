from datetime import datetime
from uuid import UUID
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema


class AnswerCommentBase(BaseSchema):
    answer_id: UUID
    comment_text: str


class AnswerCommentCreate(AnswerCommentBase):
    pass


class AnswerCommentUpdate(BaseSchema):
    comment_text: str


class AnswerComment(AnswerCommentBase, TimeStampSchema, IdSchema):
    last_modified: datetime
