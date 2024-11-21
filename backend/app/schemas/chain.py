from typing import List
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema


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
