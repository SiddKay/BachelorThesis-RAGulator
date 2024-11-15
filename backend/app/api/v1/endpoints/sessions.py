from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.session import Session
from app.schemas.session import (
    SessionCreate,
    Session as SessionSchema,
    SessionDetail,
    SessionUpdate,
)
from app.api.deps import get_db_session
from app.services.session import SessionService
from app.services.exceptions import SessionError, SessionNotFoundError

router = APIRouter(prefix="/sessions", tags=["sessions"])
logger = get_logger(__name__)


async def get_session_service(
    db: AsyncSession = Depends(get_db_session),
) -> SessionService:
    return SessionService(Session, db)


@router.post(
    "/",
    response_model=SessionSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Session created successfully"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def create_session(
    session: SessionCreate,
    service: SessionService = Depends(get_session_service),
) -> SessionSchema:
    """Create a new evaluation session."""
    try:
        eval_session = await service.create_session(session)
        return SessionSchema.model_validate(eval_session)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except SessionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/",
    response_model=List[SessionDetail],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of sessions retrieved successfully"},
        500: {"description": "Internal server error"},
    },
)
async def get_sessions(
    skip: int = 0,
    limit: int = 100,
    service: SessionService = Depends(get_session_service),
) -> List[SessionDetail]:
    """Get all evaluation sessions."""
    try:
        sessions = await service.get_sessions(skip=skip, limit=limit)
        return [SessionDetail.model_validate(s) for s in sessions]
    except SessionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/{session_id}",
    response_model=SessionDetail,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Session retrieved successfully"},
        404: {"description": "Session not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_session(
    session_id: UUID, service: SessionService = Depends(get_session_service)
) -> SessionDetail:
    """Get a specific session by ID."""
    try:
        session = await service.get_session_by_id(session_id)
        return SessionDetail.model_validate(session)
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except SessionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch(
    "/{session_id}",
    response_model=SessionSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Session updated successfully"},
        404: {"description": "Session not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def update_session(
    session_id: UUID,
    session_update: SessionUpdate,
    service: SessionService = Depends(get_session_service),
) -> SessionSchema:
    """Update a session."""
    try:
        updated_session = await service.update_session(
            session_id=session_id, data=session_update
        )
        return SessionSchema.model_validate(updated_session)
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except SessionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/{session_id}",
    response_model=SessionSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Session deleted successfully"},
        404: {"description": "Session not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_session(
    session_id: UUID, service: SessionService = Depends(get_session_service)
) -> SessionSchema:
    """Delete a session."""
    try:
        deleted_session = await service.delete_session(session_id)
        return SessionSchema.model_validate(deleted_session)
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except SessionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
