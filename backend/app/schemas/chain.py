from uuid import UUID
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema


class ChainBase(BaseSchema):
    file_path: str


class ChainCreate(ChainBase):
    pass


class Chain(ChainBase, TimeStampSchema, IdSchema):
    pass
