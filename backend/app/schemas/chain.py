from typing import List
from pydantic import Field
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema
from app.schemas.configuration import Configuration


class ChainBase(BaseSchema):
    file_name: str


class Chain(ChainBase, TimeStampSchema, IdSchema):
    configurations: List[Configuration] = Field(default_factory=list)


class AvailableChain(BaseSchema):
    """Schema for available chain files in backend/chains directory"""

    file_name: str


class ChainSelection(BaseSchema):
    """Schema for selecting chains to associate with a session"""

    file_names: List[str]
