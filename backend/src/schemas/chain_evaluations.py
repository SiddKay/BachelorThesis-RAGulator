from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class ChainEvaluationBase(BaseModel):
    """Base Pydantic model for ChainEvaluation"""

    session_id: UUID
    chain_id: UUID


class ChainEvaluationCreate(ChainEvaluationBase):
    """Pydantic model for ChainEvaluation creation"""

    pass


class ChainEvaluationRead(ChainEvaluationBase):
    """Pydantic model for ChainEvaluation reading"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
