from typing import List, Type
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.answer import Answer
from app.models.chain import Chain
from app.models.question import Question
from app.models.configuration import Configuration
from app.services.base import BaseService
from app.schemas.answer import AnswerCreate, AnswerUpdate
from app.services.exceptions import (
    AnswerError,
    AnswerNotFoundError,
    ChainNotFoundError,
    QuestionNotFoundError,
    ConfigurationNotFoundError,
)

logger = get_logger(__name__)


class AnswerService(BaseService[Answer]):
    def __init__(self, model: Type[Answer], db: AsyncSession):
        super().__init__(model, db)

    async def _validate_references(
        self,
        *,
        chain_id: UUID | None = None,
        question_id: UUID | None = None,
        configuration_id: UUID | None = None,
    ) -> bool:
        """Validate that provided entity references exist."""
        try:
            if chain_id:
                chain_result = await self.db.execute(
                    select(Chain).where(Chain.id == chain_id)
                )
                if not chain_result.scalar_one_or_none():
                    raise ChainNotFoundError(
                        f"Chain with id '{chain_id}' not found"
                    )

            if question_id:
                question_result = await self.db.execute(
                    select(Question).where(Question.id == question_id)
                )
                if not question_result.scalar_one_or_none():
                    raise QuestionNotFoundError(
                        f"Question with id '{question_id}' not found"
                    )

            if configuration_id:
                config_result = await self.db.execute(
                    select(Configuration).where(
                        Configuration.id == configuration_id
                    )
                )
                if not config_result.scalar_one_or_none():
                    raise ConfigurationNotFoundError(
                        f"Configuration with id '{configuration_id}' not found"
                    )

            return True

        except SQLAlchemyError as e:
            logger.error(
                f"Database error while validating references: {str(e)}"
            )
            raise AnswerError("Failed to validate references") from e

    async def create_answer(
        self, *, question_id: UUID, data: AnswerCreate
    ) -> Answer:
        """Create a new answer."""
        try:
            # Validate all references first
            await self._validate_references(
                chain_id=data.chain_id,
                question_id=question_id,
                configuration_id=data.configuration_id,
            )
            answer_data = data.model_dump()
            answer_data["question_id"] = question_id
            answer = await self.create(obj_data=answer_data)
            logger.info(
                f"Created answer for question '{question_id}' "
                f"using chain '{data.chain_id}' and configuration '{data.configuration_id}'"
            )
            return answer
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating answer: {str(e)}")
            raise AnswerError("Failed to create answer") from e

    async def create_answers_bulk(
        self, *, question_id: UUID, data: List[AnswerCreate]
    ) -> List[Answer]:
        """Create multiple answers for a single question."""
        try:
            # Validate question_id first
            await self._validate_references(question_id=question_id)

            # Validate other references for each answer
            all_chain_ids = {answer.chain_id for answer in data}
            all_configuration_ids = {
                answer.configuration_id for answer in data
            }

            for chain_id in all_chain_ids:
                await self._validate_references(chain_id=chain_id)
            for configuration_id in all_configuration_ids:
                await self._validate_references(
                    configuration_id=configuration_id
                )

            # Prepare bulk data
            answers_data = [
                {**answer.model_dump(), "question_id": question_id}
                for answer in data
            ]

            # Create all answers in one transaction
            answers = await self.create_bulk(objects_data=answers_data)
            return answers
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while creating answers in bulk: {str(e)}"
            )
            raise AnswerError("Failed to create answers in bulk") from e

    async def get_answers_by_question(self, question_id: UUID) -> List[Answer]:
        """Get all answers for a specific question."""
        try:
            # Validate question_id first
            await self._validate_references(question_id=question_id)
            query = select(self.model).where(
                self.model.question_id == question_id
            )
            result = await self.db.execute(query)
            answers = list(result.scalars().all())
            logger.info(
                f"Retrieved {len(answers)} answers for question '{question_id}'"
            )
            return answers
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching answers: {str(e)}")
            raise AnswerError("Failed to fetch answers") from e

    async def get_answers_by_configuration(
        self, configuration_id: UUID
    ) -> List[Answer]:
        """Get all answers for a specific configuration."""
        try:
            # Validate question_id first
            await self._validate_references(configuration_id=configuration_id)
            query = select(self.model).where(
                self.model.configuration_id == configuration_id
            )
            result = await self.db.execute(query)
            answers = list(result.scalars().all())
            logger.info(
                f"Retrieved {len(answers)} answers for configuration '{configuration_id}'"
            )
            return answers
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching answers: {str(e)}")
            raise AnswerError("Failed to fetch answers") from e

    async def get_average_score_by_configuration(
        self, configuration_id: UUID
    ) -> float:
        """Get the average score for a specific configuration. Only answers with a score are considered."""
        try:
            # Validate question_id first
            await self._validate_references(configuration_id=configuration_id)
            query = select(self.model).where(
                self.model.configuration_id == configuration_id
            )
            result = await self.db.execute(query)
            answers = list(result.scalars().all())

            # Filter answers that have a score
            scored_answers = [
                answer for answer in answers if answer.score is not None
            ]

            if not scored_answers:
                logger.info(
                    f"No scored answers found for configuration '{configuration_id}'"
                )
                return 0.0

            total_score = sum(answer.score for answer in scored_answers)
            average = total_score / len(scored_answers)

            logger.info(
                f"Retrieved average score of {average} for configuration '{configuration_id}' "
                f"(from {len(scored_answers)} scored answers out of {len(answers)} total answers)"
            )
            return average
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while fetching average score: {str(e)}"
            )
            raise AnswerError("Failed to fetch average score") from e

    async def update_answer_score(
        self, *, question_id: UUID, answer_id: UUID, data: AnswerUpdate
    ) -> Answer:
        """Update the score for a specific answer."""
        try:
            # Validate question_id first
            await self._validate_references(question_id=question_id)

            # Get and validate answer
            answer = await self.get(answer_id)
            if not answer:
                raise AnswerNotFoundError(
                    f"Answer with id '{answer_id}' not found"
                )

            if answer.question_id != question_id:
                raise AnswerNotFoundError(
                    f"Answer '{answer_id}' not found in question '{question_id}'"
                )

            # Update score
            update_data = data.model_dump(exclude_unset=True)
            updated_answer = await self.update(
                db_obj=answer, obj_data=update_data
            )

            logger.info(
                f"Updated answer '{answer_id}' score to {updated_answer.score}"
            )
            return updated_answer
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while updating answer score: {str(e)}"
            )
            raise AnswerError("Failed to update answer score") from e

    async def delete_answer(
        self, *, question_id: UUID, answer_id: UUID
    ) -> Answer:
        """Delete a specific answer."""
        try:
            # Validate question_id first
            await self._validate_references(question_id=question_id)
            answer = await self.get(answer_id)
            if not answer:
                raise AnswerNotFoundError(
                    f"Answer with id '{answer_id}' not found"
                )

            await self.delete(db_obj=answer)
            logger.warning(f"Deleted answer '{answer_id}'")
            return answer
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting answer: {str(e)}")
            raise AnswerError("Failed to delete answer") from e

    async def delete_answers_by_question(
        self, question_id: UUID
    ) -> List[Answer]:
        """Delete all answers for a specific question."""
        try:
            # Validate question_id first
            await self._validate_references(question_id=question_id)
            query = select(self.model).where(
                self.model.question_id == question_id
            )
            result = await self.db.execute(query)
            answers = list(result.scalars().all())
            await self.delete_bulk(db_objects=answers)
            logger.warning(
                f"Deleted {len(answers)} answers for question '{question_id}'"
            )
            return answers
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting answers: {str(e)}")
            raise AnswerError("Failed to delete answers") from e
