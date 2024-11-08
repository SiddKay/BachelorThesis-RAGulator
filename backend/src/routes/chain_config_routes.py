from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from src.models.chain_config import *
from src.services.chain_loader import ChainLoader
from src.services.parameter_manager import ParameterManager
from src.services.prompt_manager import PromptManager


router = APIRouter()
chain_loader = ChainLoader()
parameter_manager = ParameterManager(chain_loader)
prompt_manager = PromptManager(chain_loader)


@router.get("/chains", response_model=List[str])
async def list_chains():
    """Get list of available chains."""
    return chain_loader.list_available_chains()


@router.get("/chains/{chain_name}/parameters", response_model=ChainResponse)
async def get_chain_parameters(chain_name: str):
    """Get current model parameters for a specific chain."""
    try:
        parameters = parameter_manager.get_chain_parameters(chain_name)
        return ChainResponse(
            chain_name=chain_name,
            parameters=parameters,
            message="Parameters retrieved successfully",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )


@router.put("/chains/parameters", response_model=ChainResponse)
async def update_chain_parameters(update_data: ChainParameterUpdate):
    """Update model parameters for a specific chain."""
    try:
        updated_params = parameter_manager.update_chain_parameters(
            update_data.chain_name, update_data.parameters
        )
        return ChainResponse(
            chain_name=update_data.chain_name,
            parameters=updated_params,
            message="Parameter updated successfully",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )


@router.get("/chains/{chain_name}/prompt", response_model=ChainResponse)
async def get_chain_prompt(chain_name: str):
    """Get current prompt template for a specific chain."""
    try:
        prompt_template = prompt_manager.get_prompt_template(chain_name)
        return ChainResponse(
            chain_name=chain_name,
            data=prompt_template,
            message="Prompt template retrieved successfully",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )


@router.put("/chains/prompt", response_model=ChainResponse)
async def update_chain_prompt(update_data: PromptUpdate):
    """Update prompt template for a specific chain."""
    try:
        updated_prompt = prompt_manager.update_prompt_template(
            update_data.chain_name, update_data.template_config
        )
        return ChainResponse(
            chain_name=update_data.chain_name,
            data=updated_prompt,
            message="Prompt template updated successfully",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )
