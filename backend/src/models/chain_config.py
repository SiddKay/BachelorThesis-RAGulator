from pydantic import BaseModel
from typing import Any, Dict, Optional


class ChainParameterUpdate(BaseModel):
    chain_name: str
    parameters: Dict[str, Any]


class PromptUpdate(BaseModel):
    chain_name: str
    template_config: Dict[str, Any]


class ChainResponse(BaseModel):
    chain_name: str
    data: Dict[str, Any]
    message: Optional[str] = None
