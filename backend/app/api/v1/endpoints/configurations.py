from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.configuration import Configuration
from app.schemas.configuration import (
    Configuration as ConfigurationSchema,
    ConfigurationCreate,
    ConfigurationUpdate,
    ConfigSchema,
)
from app.api.deps import get_db_session
from app.services.configuration import ConfigurationService
from app.services.exceptions import (
    SessionNotFoundError,
    ConfigurationError,
    ConfigurationNotFoundError,
    ChainNotFoundError,
)

router = APIRouter(
    prefix="/sessions/{session_id}/chains/{chain_id}/configurations",
    tags=["configurations"],
)
logger = get_logger(__name__)


async def get_configuration_service(
    db: AsyncSession = Depends(get_db_session),
) -> ConfigurationService:
    return ConfigurationService(Configuration, db)


@router.get(
    "/schema",
    response_model=ConfigSchema,
    responses={
        200: {"description": "Configuration schema retrieved successfully"},
        404: {"description": "Chain not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_config_schema(
    session_id: UUID,
    chain_id: UUID,
    service: ConfigurationService = Depends(get_configuration_service),
) -> ConfigSchema:
    """Get the configuration schema for a chain."""
    try:
        schema = await service.get_chain_schema(
            session_id=session_id, chain_id=chain_id
        )
        return schema
    except (ChainNotFoundError, SessionNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "",
    response_model=ConfigurationSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Configuration created successfully"},
        404: {"description": "Session or chain not found"},
        400: {"description": "Invalid configuration values"},
    },
)
async def create_configuration(
    session_id: UUID,
    chain_id: UUID,
    config_in: ConfigurationCreate,
    service: ConfigurationService = Depends(get_configuration_service),
) -> ConfigurationSchema:
    """Create a new configuration for a chain."""
    try:
        config = await service.create_configuration(
            session_id=session_id, chain_id=chain_id, data=config_in
        )
        return ConfigurationSchema.model_validate(config)
    except (SessionNotFoundError, ChainNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "",
    response_model=List[ConfigurationSchema],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Configurations retrieved successfully"},
        404: {"description": "Session or chain not found"},
    },
)
async def list_configurations(
    session_id: UUID,
    chain_id: UUID,
    service: ConfigurationService = Depends(get_configuration_service),
) -> List[ConfigurationSchema]:
    """List all configurations for a chain."""
    try:
        configs = await service.get_chain_configurations(
            session_id=session_id, chain_id=chain_id
        )
        return [
            ConfigurationSchema.model_validate(config) for config in configs
        ]
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/{config_id}",
    response_model=ConfigurationSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Configuration retrieved successfully"},
        404: {"description": "Configuration not found"},
    },
)
async def get_configuration(
    session_id: UUID,
    config_id: UUID,
    service: ConfigurationService = Depends(get_configuration_service),
) -> ConfigurationSchema:
    """Get a specific configuration by ID."""
    try:
        config = await service.get_configuration_by_id(
            session_id=session_id, config_id=config_id
        )
        return ConfigurationSchema.model_validate(config)
    except (SessionNotFoundError, ConfigurationNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.put(
    "/{config_id}",
    response_model=ConfigurationSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Configuration updated successfully"},
        404: {"description": "Configuration not found"},
        400: {"description": "Invalid configuration values"},
    },
)
async def update_configuration(
    session_id: UUID,
    chain_id: UUID,
    config_id: UUID,
    config_update: ConfigurationUpdate,
    service: ConfigurationService = Depends(get_configuration_service),
) -> ConfigurationSchema:
    """Update an existing configuration."""
    try:
        config = await service.update_configuration(
            session_id=session_id,
            chain_id=chain_id,
            config_id=config_id,
            data=config_update,
        )
        return ConfigurationSchema.model_validate(config)
    except (
        SessionNotFoundError,
        ChainNotFoundError,
        ConfigurationNotFoundError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete(
    "/{config_id}",
    response_model=ConfigurationSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Configuration deleted successfully"},
        404: {"description": "Configuration not found"},
    },
)
async def delete_configuration(
    session_id: UUID,
    config_id: UUID,
    service: ConfigurationService = Depends(get_configuration_service),
) -> ConfigurationSchema:
    """Delete a specific configuration."""
    try:
        config = await service.delete_configuration(
            session_id=session_id, config_id=config_id
        )
        return ConfigurationSchema.model_validate(config)
    except (
        SessionNotFoundError,
        ChainNotFoundError,
        ConfigurationNotFoundError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
