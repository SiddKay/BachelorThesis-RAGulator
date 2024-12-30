from typing import Optional, Dict, Any
from app.schemas.base import BaseSchema, TimeStampSchema, IdSchema


class ConfigurationBase(BaseSchema):
    config_values: Optional[Dict[str, Any]] = None


class ConfigSchema(BaseSchema):
    config_schema: Optional[Dict[str, Any]] = None


class ConfigurationCreate(ConfigurationBase):
    pass


class ConfigurationUpdate(ConfigurationBase):
    pass


class Configuration(ConfigurationBase, TimeStampSchema, IdSchema):
    pass
