from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID


class ConfigurationBase(BaseModel):
    """Base Pydantic model for Configuration"""

    prompt_template: Optional[Dict] = None
    model_params: Optional[Dict] = None


class ConfigurationCreate(ConfigurationBase):
    """Pydantic model for Configuration creation"""

    pass


class ConfigurationRead(ConfigurationBase):
    """Pydantic model for Configuration reading"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
