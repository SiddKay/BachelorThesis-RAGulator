from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.answer import Answer
from app.schemas.answer import (
    Answer as AnswerSchema,
    AnswerCreate,
    AnswerBulkCreate,
    AnswerDetail,
    AnswerUpdate,
)
from app.api.deps import get_db_session
from app.services.answer import AnswerService
from app.services.exceptions import (
    AnswerError,
    AnswerNotFoundError,
    ChainNotFoundError,
    QuestionNotFoundError,
    ConfigurationNotFoundError,
)

router = APIRouter(tags=["answers"])
logger = get_logger(__name__)


async def get_answer_service(
    db: AsyncSession = Depends(get_db_session),
) -> AnswerService:
    return AnswerService(Answer, db)


@router.post(
    "/questions/{question_id}/answers/bulk",
    response_model=List[AnswerSchema],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Answers created successfully"},
        404: {"description": "Referenced entity not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def create_answers_bulk(
    question_id: UUID,
    answers_in: AnswerBulkCreate,
    service: AnswerService = Depends(get_answer_service),
) -> List[AnswerSchema]:
    """Create multiple answers for a question."""
    try:
        answers = await service.create_answers_bulk(
            question_id=question_id, data=answers_in.answers
        )
        return [AnswerSchema.model_validate(answer) for answer in answers]
    except (
        ChainNotFoundError,
        QuestionNotFoundError,
        ConfigurationNotFoundError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except AnswerError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/questions/{question_id}/answers",
    response_model=AnswerSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Answer created successfully"},
        404: {"description": "Referenced entity not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def create_answer(
    question_id: UUID,
    answer_in: AnswerCreate,
    service: AnswerService = Depends(get_answer_service),
) -> AnswerSchema:
    """Create a new answer."""
    try:
        answer = await service.create_answer(
            question_id=question_id, data=answer_in
        )
        return AnswerSchema.model_validate(answer)
    except (
        ChainNotFoundError,
        QuestionNotFoundError,
        ConfigurationNotFoundError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except AnswerError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/questions/{question_id}/answers",
    response_model=List[AnswerDetail],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Answers retrieved successfully"},
        404: {"description": "Question not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_answers_for_question(
    question_id: UUID,
    service: AnswerService = Depends(get_answer_service),
) -> List[AnswerDetail]:
    """Get all answers for a specific question."""
    try:
        answers = await service.get_answers_by_question(question_id)
        return [AnswerDetail.model_validate(answer) for answer in answers]
    except QuestionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AnswerError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/configurations/{configuration_id}/answers",
    response_model=List[AnswerDetail],
    responses={
        200: {"description": "Answers retrieved successfully"},
        404: {"description": "Configuration not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_answers_for_configuration(
    configuration_id: UUID,
    service: AnswerService = Depends(get_answer_service),
) -> List[AnswerDetail]:
    """Get all answers for a specific configuration."""
    try:
        answers = await service.get_answers_by_configuration(configuration_id)
        return [AnswerDetail.model_validate(answer) for answer in answers]
    except ConfigurationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AnswerError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/configurations/{configuration_id}/score",
    response_model=float,
    responses={
        200: {"description": "Average score retrieved successfully"},
        404: {"description": "Configuration not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_configuration_average_score(
    configuration_id: UUID,
    service: AnswerService = Depends(get_answer_service),
) -> float:
    """Get the average score for answers with a specific configuration."""
    try:
        return await service.get_average_score_by_configuration(
            configuration_id
        )
    except ConfigurationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AnswerError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch(
    "/questions/{question_id}/answers/{answer_id}",
    response_model=AnswerDetail,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Answer updated successfully"},
        404: {"description": "Answer not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
async def update_answer_score(
    question_id: UUID,
    answer_id: UUID,
    answer_update: AnswerUpdate,
    service: AnswerService = Depends(get_answer_service),
) -> AnswerDetail:
    """Update an answer's score."""
    try:
        answer = await service.update_answer_score(
            question_id=question_id,
            answer_id=answer_id,
            data=answer_update,
        )
        return AnswerDetail.model_validate(answer, from_attributes=True)
    except (AnswerNotFoundError, QuestionNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except AnswerError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/questions/{question_id}/answers/{answer_id}",
    response_model=AnswerSchema,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Answer deleted successfully"},
        404: {"description": "Answer not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_answer(
    question_id: UUID,
    answer_id: UUID,
    service: AnswerService = Depends(get_answer_service),
) -> AnswerSchema:
    """Delete a specific answer."""
    try:
        answer = await service.delete_answer(
            question_id=question_id, answer_id=answer_id
        )
        return AnswerSchema.model_validate(answer)
    except (AnswerNotFoundError, QuestionNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AnswerError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/questions/{question_id}/answers",
    response_model=List[AnswerSchema],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "All answers for question deleted successfully"},
        404: {"description": "Question not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_all_question_answers(
    question_id: UUID,
    service: AnswerService = Depends(get_answer_service),
) -> List[AnswerSchema]:
    """Delete all answers for a specific question."""
    try:
        answers = await service.delete_answers_by_question(question_id)
        return [AnswerDetail.model_validate(answer) for answer in answers]
    except QuestionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except AnswerError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
