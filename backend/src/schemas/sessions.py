from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


class SessionBase(BaseModel):
    """Base Pydantic model for Session"""

    name: str
    description: Optional[str] = None


class SessionCreate(SessionBase):
    """Pydantic model for Session creation"""

    pass


class SessionRead(SessionBase):
    """Pydantic model for Session reading"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    last_accessed: datetime
