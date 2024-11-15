from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import get_session
from app.models import models
from app.schemas import schemas

router = APIRouter()


@router.post(
    "/sessions/",
    response_model=schemas.Session,
    summary="Create a new session",
    status_code=201,
)
async def create_session(
    session: schemas.SessionCreate, db: AsyncSession = Depends(get_session)
) -> schemas.Session:
    """
    Create a new session with the provided data.
    """
    try:
        db_session = models.Session(**session.model_dump())
        db.add(db_session)
        await db.commit()
        await db.refresh(db_session)
        return db_session

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to create session: " + str(e)
        )


@router.post(
    "/sessions/{session_id}/questions/", response_model=schemas.Question
)
async def create_question(
    session_id: int,
    question: schemas.QuestionCreate,
    db: AsyncSession = Depends(get_session),
):
    db_question = models.Question(
        session_id=session_id, content=question.content
    )
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question


@router.post(
    "/questions/{question_id}/answers/", response_model=schemas.Answer
)
async def create_answer(
    question_id: int,
    answer: schemas.AnswerCreate,
    db: AsyncSession = Depends(get_session),
):
    db_answer = models.Answer(question_id=question_id, content=answer.content)
    db.add(db_answer)
    await db.commit()
    await db.refresh(db_answer)
    return db_answer


@router.get("/sessions/{session_id}", response_model=schemas.Session)
async def get_session(
    session_id: int, db: AsyncSession = Depends(get_session)
):
    query = select(models.Session).where(models.Session.id == session_id)
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session
