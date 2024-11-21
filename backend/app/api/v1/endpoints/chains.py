from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.chain import Chain
from app.schemas.chain import (
    Chain as ChainSchema,
    AvailableChain,
    ChainSelection,
)
from app.api.deps import get_db_session
from app.services.chain import ChainService
from app.services.exceptions import (
    ChainError,
    ChainNotFoundError,
    SessionNotFoundError,
)

router = APIRouter(tags=["chains"])
logger = get_logger(__name__)


async def get_session_service(
    db: AsyncSession = Depends(get_db_session),
) -> ChainService:
    return ChainService(Chain, db)


@router.get(
    "/available-chains",
    response_model=List[AvailableChain],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Available chain files retrieved successfully"},
        500: {"description": "Internal server error"},
    },
)
async def get_available_chains(
    service: ChainService = Depends(get_session_service),
) -> List[AvailableChain]:
    """Get all available chain files from backend/chains directory."""
    try:
        chain_files = await service.get_available_chains()
        return [AvailableChain(file_name=path) for path in chain_files]
    except ChainError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/sessions/{session_id}/select-chains",
    response_model=List[ChainSchema],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Chains selected successfully"},
        404: {"description": "Session not found"},
        400: {"description": "Invalid chain selection"},
        500: {"description": "Internal server error"},
    },
)
async def select_chains(
    session_id: UUID,
    selection: ChainSelection,
    service: ChainService = Depends(get_session_service),
) -> List[ChainSchema]:
    """Select chain files for evaluation."""
    try:
        chains = await service.select_chains(
            session_id=session_id,
            file_names=selection.file_names,
        )
        return [ChainSchema.model_validate(chain) for chain in chains]
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ChainError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/sessions/{session_id}/chains",
    response_model=List[ChainSchema],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Chains retrieved"},
        404: {"description": "Session not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_session_chains(
    session_id: UUID,
    service: ChainService = Depends(get_session_service),
) -> List[ChainSchema]:
    """Get all chains for a session."""
    try:
        chains = await service.get_session_chains(session_id)
        return [ChainSchema.model_validate(chain) for chain in chains]
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ChainError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/sessions/{session_id}/chains/{chain_id}",
    response_model=ChainSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Chain deleted successfully"},
        404: {"description": "Chain not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_session_chain(
    session_id: UUID,
    chain_id: UUID,
    service: ChainService = Depends(get_session_service),
) -> ChainSchema:
    """Delete a specific chain from a session."""
    try:
        chain = await service.delete_session_chain(
            session_id=session_id, chain_id=chain_id
        )
        return ChainSchema.model_validate(chain)
    except (SessionNotFoundError, ChainNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ChainError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/sessions/{session_id}/chains",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Chains deleted successfully"},
        404: {"description": "Session not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_session_chains(
    session_id: UUID,
    service: ChainService = Depends(get_session_service),
) -> None:
    """Delete all chains for a session."""
    try:
        await service.delete_session_chains(session_id)
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ChainError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
