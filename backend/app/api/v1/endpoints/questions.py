from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.question import Question
from app.schemas.question import (
    Question as QuestionSchema,
    QuestionCreate,
    QuestionBulkCreate,
    QuestionUpdate,
    QuestionBulkDelete,
    QuestionDetail,
)
from app.api.deps import get_db_session
from app.services.question import QuestionService
from app.services.exceptions import (
    QuestionError,
    QuestionNotFoundError,
    SessionNotFoundError,
)

router = APIRouter(prefix="/sessions/{session_id}", tags=["questions"])
logger = get_logger(__name__)


async def get_question_service(
    db: AsyncSession = Depends(get_db_session),
) -> QuestionService:
    return QuestionService(Question, db)


@router.post(
    "/questions/bulk",
    response_model=List[QuestionSchema],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Questions created successfully"},
        404: {"description": "Session not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def create_questions_bulk(
    session_id: UUID,
    questions_in: QuestionBulkCreate,
    service: QuestionService = Depends(get_question_service),
) -> List[QuestionSchema]:
    """Create multiple questions in a session."""
    try:
        questions = await service.create_questions_bulk(
            session_id=session_id, data=questions_in.questions
        )
        # Use from_orm to properly handle relationships when returning QuestionDetail instead of QuestionSchema
        # return [
        #     QuestionSchema.model_validate(question, from_attributes=True)
        #     for question in questions
        # ]
        return [QuestionSchema.model_validate(q) for q in questions]
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except QuestionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/questions/bulk",  # Keep bulk delete before dynamic routes
    response_model=List[QuestionSchema],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Questions deleted successfully"},
        404: {"description": "Session not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def delete_questions_bulk(
    session_id: UUID,
    questions_in: QuestionBulkDelete,
    service: QuestionService = Depends(get_question_service),
) -> List[QuestionSchema]:
    """Delete multiple questions from a session."""
    try:
        questions = await service.delete_questions_bulk(
            session_id=session_id, question_ids=questions_in.question_ids
        )
        return [QuestionSchema.model_validate(q) for q in questions]
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except QuestionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/questions",
    response_model=QuestionSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Question created successfully"},
        404: {"description": "Session not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def create_question(
    session_id: UUID,
    question_in: QuestionCreate,
    service: QuestionService = Depends(get_question_service),
) -> QuestionSchema:
    """Create a new question in a session."""
    try:
        question = await service.create_question(
            session_id=session_id, data=question_in
        )
        return QuestionSchema.model_validate(question)
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except QuestionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/questions",
    response_model=List[QuestionDetail],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Questions retrieved successfully"},
        404: {"description": "Session not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_session_questions(
    session_id: UUID,
    service: QuestionService = Depends(get_question_service),
) -> List[QuestionDetail]:
    """Get all questions for a session."""
    try:
        questions = await service.get_session_questions(session_id)
        return [
            QuestionDetail.model_validate(question) for question in questions
        ]
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except QuestionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch(
    "/questions/{question_id}",
    response_model=QuestionDetail,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Question updated successfully"},
        404: {"description": "Question not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def update_question(
    session_id: UUID,
    question_id: UUID,
    question_update: QuestionUpdate,
    service: QuestionService = Depends(get_question_service),
) -> QuestionDetail:
    """Update a specific question."""
    try:
        question = await service.update_question(
            session_id=session_id,
            question_id=question_id,
            data=question_update,
        )
        return QuestionDetail.model_validate(question)
    except (SessionNotFoundError, QuestionNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except QuestionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/questions/{question_id}",
    response_model=QuestionSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Question deleted successfully"},
        404: {"description": "Question not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_question(
    session_id: UUID,
    question_id: UUID,
    service: QuestionService = Depends(get_question_service),
) -> QuestionSchema:
    """Delete a specific question."""
    try:
        question = await service.delete_question(
            session_id=session_id, question_id=question_id
        )
        return QuestionSchema.model_validate(question)
    except (SessionNotFoundError, QuestionNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except QuestionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/questions",
    response_model=List[QuestionSchema],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "All questions deleted successfully"},
        404: {"description": "Session not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_session_questions(
    session_id: UUID,
    service: QuestionService = Depends(get_question_service),
) -> List[QuestionSchema]:
    """Delete all questions for a session."""
    try:
        questions = await service.delete_session_questions(session_id)
        return [QuestionSchema.model_validate(q) for q in questions]
    except SessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except QuestionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
