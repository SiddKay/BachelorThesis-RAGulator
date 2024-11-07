from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class ChainBase(BaseModel):
    """Base Pydantic model for Chain"""

    file_name: str
    file_path: str


class ChainCreate(ChainBase):
    """Pydantic model for Chain creation"""

    pass


class ChainRead(ChainBase):
    """Pydantic model for Chain reading"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    imported_at: datetime
