from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Any, Dict, Optional, List
from uuid import UUID


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimeStampSchema(BaseSchema):
    created_at: datetime


class IdSchema(BaseSchema):
    id: UUID


# Chains API
class ChainBase(BaseSchema):
    file_name: str


class Chain(ChainBase, TimeStampSchema, IdSchema):
    pass


class AvailableChain(BaseSchema):
    """Schema for available chain files in backend/chains directory"""

    file_name: str


class ChainSelection(BaseSchema):
    """Schema for selecting chains to associate with a session"""

    file_names: List[str]


# Configurations API
class ConfigurationBase(BaseSchema):
    prompt_template: Optional[Dict[str, Any]] = None
    llm_parameters: Optional[Dict[str, Any]] = None


class ConfigurationCreate(ConfigurationBase):
    pass


class ConfigurationUpdate(BaseSchema):
    prompt_template: Optional[Dict[str, Any]] = None
    llm_parameters: Optional[Dict[str, Any]] = None


class Configuration(ConfigurationBase, TimeStampSchema, IdSchema):
    pass


# Answer Comments API
class AnswerCommentBase(BaseSchema):
    answer_id: UUID
    comment_text: str


class AnswerCommentCreate(AnswerCommentBase):
    pass


class AnswerCommentUpdate(BaseSchema):
    comment_text: str


class AnswerComment(AnswerCommentBase, TimeStampSchema, IdSchema):
    last_modified: datetime


# Answers API
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


# Questions API
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


# Sessions API
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
