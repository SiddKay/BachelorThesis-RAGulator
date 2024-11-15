from typing import Optional, Dict, Any
from uuid import UUID
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema


class ConfigurationBase(BaseSchema):
    session_id: UUID
    prompt_template: Optional[Dict[str, Any]] = None
    llm_parameters: Optional[Dict[str, Any]] = None


class ConfigurationCreate(ConfigurationBase):
    pass


class ConfigurationUpdate(BaseSchema):
    prompt_template: Optional[Dict[str, Any]] = None
    llm_parameters: Optional[Dict[str, Any]] = None


class Configuration(ConfigurationBase, TimeStampSchema, IdSchema):
    pass
