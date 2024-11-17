from typing import Optional, Dict, Any
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema


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
