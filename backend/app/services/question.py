from typing import List, Type
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.question import Question
from app.models.session import Session
from app.services.base import BaseService
from app.schemas.question import QuestionCreate, QuestionUpdate
from app.services.exceptions import (
    QuestionError,
    QuestionNotFoundError,
    SessionNotFoundError,
)

logger = get_logger(__name__)


class QuestionService(BaseService[Question]):
    def __init__(self, model: Type[Question], db: AsyncSession):
        super().__init__(model, db)
        self.session_model = Session

    async def _validate_session(self, session_id: UUID) -> bool:
        """Validate if the session exists."""
        try:
            query = select(self.session_model).where(
                self.session_model.id == session_id
            )
            result = await self.db.execute(query)
            session = result.scalar_one_or_none()
            if not session:
                raise SessionNotFoundError(
                    f"Session with id '{session_id}' not found"
                )
            return True
        except SQLAlchemyError as e:
            logger.error(f"Database error while validating session: {str(e)}")
            raise QuestionError("Failed to validate session") from e

    async def _validate_session_question(
        self, *, session_id: UUID, question_id: UUID
    ) -> Question:
        """Validate that the question belongs to the session."""
        try:
            await self._validate_session(session_id)
            question = await self.get(question_id)

            if not question:
                raise QuestionNotFoundError(
                    f"Question '{question_id}' not found"
                )

            if question.session_id != session_id:
                raise QuestionNotFoundError(
                    f"Question '{question_id}' not found in session '{session_id}'"
                )

            return question
        except SQLAlchemyError as e:
            logger.error(f"Database error while validating question: {str(e)}")
            raise QuestionError("Failed to validate question") from e

    async def create_question(
        self, *, session_id: UUID, data: QuestionCreate
    ) -> Question:
        """Create a new question within a session."""
        try:
            # Validate that the session exists
            await self._validate_session(session_id)
            question_data = (
                data.model_dump()
            )  # TODO: check if exclude_unset=True is needed
            question_data["session_id"] = session_id
            question = await self.create(obj_data=question_data)
            logger.info(f"Created question in session '{session_id}'")
            return question
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating question: {str(e)}")
            raise QuestionError("Failed to create question") from e

    async def create_questions_bulk(
        self, *, session_id: UUID, data: List[QuestionCreate]
    ) -> List[Question]:
        """Create multiple questions within a session."""
        try:
            await self._validate_session(session_id)
            questions_data = [
                {**question.model_dump(), "session_id": session_id}
                for question in data
            ]
            questions = await self.create_bulk(objects_data=questions_data)

            # Force load answers relationship for each question in case of returning QuestionDetail instead of Question
            # for question in questions:
            #     await self.db.refresh(question, attribute_names=["answers"])

            return questions
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while creating questions in bulk: {str(e)}"
            )
            raise QuestionError("Failed to create questions in bulk") from e

    async def get_session_questions(self, session_id: UUID) -> List[Question]:
        """Get all questions for a specific session."""
        try:
            await self._validate_session(session_id)
            query = select(self.model).where(
                self.model.session_id == session_id
            )
            result = await self.db.execute(query)
            questions = list(result.scalars().all())
            logger.info(
                f"Retrieved {len(questions)} questions for session '{session_id}'"
            )
            return questions
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching questions: {str(e)}")
            raise QuestionError("Failed to fetch questions") from e

    async def update_question(
        self, *, session_id: UUID, question_id: UUID, data: QuestionUpdate
    ) -> Question:
        """Update an existing question."""
        try:
            question = await self._validate_session_question(
                session_id=session_id, question_id=question_id
            )
            update_data = data.model_dump(exclude_unset=True)
            return await self.update(db_obj=question, obj_data=update_data)
        except SQLAlchemyError as e:
            logger.error(f"Database error while updating question: {str(e)}")
            raise QuestionError("Failed to update question") from e

    async def delete_question(
        self, *, session_id: UUID, question_id: UUID
    ) -> Question:
        """Delete a specific question."""
        try:
            question = await self._validate_session_question(
                session_id=session_id, question_id=question_id
            )
            await self.delete(db_obj=question)
            logger.warning(
                f"Deleted question '{question_id}' from session '{session_id}'"
            )
            return question
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting question: {str(e)}")
            raise QuestionError("Failed to delete question") from e

    async def delete_questions_bulk(
        self, *, session_id: UUID, question_ids: List[UUID]
    ) -> List[Question]:
        """Delete multiple questions at once from a session."""
        try:
            # First validate all questions
            deleted_questions = []
            for question_id in question_ids:
                try:
                    question = await self._validate_session_question(
                        session_id=session_id, question_id=question_id
                    )
                    deleted_questions.append(question)
                except QuestionNotFoundError:
                    logger.warning(
                        f"Question '{question_id}' not found in session '{session_id}', skipping..."
                    )
                    continue

            if deleted_questions:
                logger.warning(
                    f"Deleting {len(deleted_questions)} questions from session '{session_id}'"
                )
                return await self.delete_bulk(db_objects=deleted_questions)
            return []
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while deleting questions in bulk: {str(e)}"
            )
            raise QuestionError("Failed to delete questions in bulk") from e

    async def delete_session_questions(
        self, session_id: UUID
    ) -> List[Question]:
        """Delete all questions for a specific session."""
        try:
            await self._validate_session(session_id)
            query = select(self.model).where(
                self.model.session_id == session_id
            )
            result = await self.db.execute(query)
            questions = list(result.scalars().all())
            await self.delete_bulk(db_objects=questions)
            logger.warning(f"Deleted all questions for session '{session_id}'")
            return questions
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting questions: {str(e)}")
            raise QuestionError("Failed to delete questions") from e
