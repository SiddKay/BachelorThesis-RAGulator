from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimeStampSchema(BaseSchema):
    created_at: datetime


class IdSchema(BaseSchema):
    id: UUID
