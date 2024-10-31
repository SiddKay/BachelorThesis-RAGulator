from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..services.extract_chain_config_service import ChainConfigService

router = APIRouter(prefix="/chain-config", tags=["chain-config"])
service = ChainConfigService()


@router.get("/all")
async def get_all_chain_configs() -> List[Dict[str, Any]]:
    """Get configurations for all available chains."""
    try:
        return service.get_all_chain_configs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chain_name}")
async def get_chain_config(chain_name: str) -> Dict[str, Any]:
    """Get configuration for a specific chain."""
    try:
        return service.get_chain_config(chain_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
