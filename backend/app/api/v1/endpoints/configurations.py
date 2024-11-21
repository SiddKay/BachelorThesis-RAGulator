from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.configuration import Configuration
from app.schemas.configuration import (
    Configuration as ConfigurationSchema,
    ConfigurationCreate,
    ConfigurationUpdate,
)
from app.api.deps import get_db_session
from app.services.configuration import ConfigurationService
from app.services.exceptions import (
    SessionNotFoundError,
    ConfigurationError,
    ConfigurationNotFoundError,
)

router = APIRouter(prefix="/sessions/{session_id}", tags=["configurations"])
logger = get_logger(__name__)


async def get_configuration_service(
    db: AsyncSession = Depends(get_db_session),
) -> ConfigurationService:
    return ConfigurationService(Configuration, db)


@router.post(
    "/configurations",
    response_model=ConfigurationSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Configuration created successfully"},
        404: {"description": "Session not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def create_configuration(
    session_id: UUID,
    config_in: ConfigurationCreate,
    service: ConfigurationService = Depends(get_configuration_service),
) -> ConfigurationSchema:
    """Create a new configuration for a session."""
    try:
        config = await service.create_configuration(
            session_id=session_id, data=config_in
        )
        return ConfigurationSchema.model_validate(config)
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/configurations",
    response_model=List[ConfigurationSchema],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Configurations retrieved successfully"},
        404: {"description": "Session not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_session_configurations(
    session_id: UUID,
    service: ConfigurationService = Depends(get_configuration_service),
) -> List[ConfigurationSchema]:
    """Get all configurations for a session."""
    try:
        configs = await service.get_session_configurations(session_id)
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
    "/configurations/{config_id}",
    response_model=ConfigurationSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Configuration retrieved successfully"},
        404: {"description": "Configuration not found"},
        500: {"description": "Internal server error"},
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
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch(
    "/configurations/{config_id}",
    response_model=ConfigurationSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Configuration updated successfully"},
        400: {"description": "Bad request"},
        404: {"description": "Configuration not found"},
        500: {"description": "Internal server error"},
    },
)
async def update_configuration(
    session_id: UUID,
    config_id: UUID,
    config_update: ConfigurationUpdate,
    service: ConfigurationService = Depends(get_configuration_service),
) -> ConfigurationSchema:
    """Update an existing configuration."""
    try:
        config = await service.update_configuration(
            session_id=session_id, config_id=config_id, data=config_update
        )
        return ConfigurationSchema.model_validate(config)
    except (SessionNotFoundError, ConfigurationNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/configurations/{config_id}",
    response_model=ConfigurationSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Configuration deleted successfully"},
        404: {"description": "Configuration not found"},
        500: {"description": "Internal server error"},
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
    except (SessionNotFoundError, ConfigurationNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
