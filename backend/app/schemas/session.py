from datetime import datetime
from typing import Optional, List
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema
from app.schemas.chain import Chain
from app.schemas.question import QuestionDetail
from app.schemas.configuration import Configuration


class SessionBase(BaseSchema):
    name: str
    description: Optional[str] = None


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SessionBase):
    name: Optional[str] = None
    description: Optional[str] = None


class Session(SessionBase, TimeStampSchema, IdSchema):
    last_modified: datetime


class SessionDetail(Session):
    chains: List[Chain] = []
    questions: List[QuestionDetail] = []
    configurations: List[Configuration] = []
