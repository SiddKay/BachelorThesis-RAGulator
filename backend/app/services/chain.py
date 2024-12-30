from typing import List, Type
import os
import aiohttp
from uuid import UUID
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.session import Session
from app.models.chain import Chain
from app.models.question import Question
from app.models.configuration import Configuration
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate
from app.services.base import BaseService
from app.services.question import QuestionService
from app.services.answer import AnswerService
from app.services.configuration import ConfigurationService
from app.services.exceptions import (
    ChainError,
    ChainNotFoundError,
    SessionNotFoundError,
)

logger = get_logger(__name__)


class ChainService(BaseService[Chain]):
    def __init__(self, model: Type[Chain], db: AsyncSession):
        super().__init__(model, db)
        self.session_model = Session

    async def _validate_session(self, session_id: UUID) -> bool:
        """Check if session exists using Session model."""
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
            raise ChainError("Failed to validate session") from e

    async def _validate_session_chain(
        self, *, session_id: UUID, chain_id: UUID
    ) -> Chain:
        """Validate that chain belongs to session."""
        try:
            await self._validate_session(session_id)
            chain = await self.get(chain_id)

            if not chain:
                raise ChainNotFoundError(f"Chain '{chain_id}' not found")

            if chain.session_id != session_id:
                raise ChainNotFoundError(
                    f"Chain '{chain_id}' not found in session '{session_id}'"
                )

            return chain
        except SQLAlchemyError as e:
            logger.error(f"Database error while validating chain: {str(e)}")
            raise ChainError("Failed to validate chain") from e

    async def _validate_chain_files(self, file_names: List[str]) -> None:
        """Validate that all chain files exist in backend/chains directory."""
        available_chains = await self.get_available_chains()
        invalid_files = [f for f in file_names if f not in available_chains]

        if invalid_files:
            raise ChainError(
                f"Chain files not found in 'backend/chains' directory: {', '.join(invalid_files)}"
            )

    async def _get_existing_chain_files(self, session_id: UUID) -> List[str]:
        """Get list of chain files already associated with session."""
        try:
            query = select(self.model.file_name).where(
                self.model.session_id == session_id
            )
            result = await self.db.execute(query)
            return [r[0] for r in result.all()]
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while fetching existing chains: {str(e)}"
            )
            raise ChainError("Failed to fetch existing chains") from e

    def _normalize_chain_name(self, chain_name: str) -> str:
        """Normalize chain name by removing .py extension if present."""
        return chain_name[:-3] if chain_name.endswith(".py") else chain_name

    async def get_available_chains(self) -> List[str]:
        """Get all available chain files from backend/chains directory."""
        try:
            # Get project root directory by going up from current service file
            service_dir = Path(__file__).resolve().parent
            backend_dir = service_dir.parent.parent
            chains_dir = backend_dir / "langserver" / "chains"

            logger.info(f"Scanning chains directory: {chains_dir}")

            # Validate directory exists
            if not chains_dir.exists():
                logger.error(f"Chains directory not found: {chains_dir}")
                raise ChainError(f"Chains directory not found: {chains_dir}")

            # Get all .py files
            chain_files = []
            for f in chains_dir.glob("*.py"):
                if f.is_file():
                    # Only return filename relative to chains dir
                    chain_files.append(f.name)
                    logger.info(f"Found chain file: {f.name}")

            logger.info(f"Found {len(chain_files)} chain files")
            return chain_files
        except Exception as e:
            logger.error(f"Error scanning chains directory: {str(e)}")
            raise ChainError("Failed to scan chains directory") from e

    async def select_chains(
        self, session_id: UUID, file_names: List[str]
    ) -> List[Chain]:
        """Associate selected chain files with a session."""
        try:
            # Verify session exists
            await self._validate_session(session_id)

            # Verify all files exist in chains directory
            await self._validate_chain_files(file_names)

            # Normalize file names by removing .py extension
            file_names = [self._normalize_chain_name(f) for f in file_names]

            # Get existing chain files for this session
            existing_files = await self._get_existing_chain_files(session_id)

            # Filter out duplicates
            new_files = [f for f in file_names if f not in existing_files]

            if not new_files:
                logger.info("No new chain files to add - all already exist")
                return []

            # Create chain objects only for new files
            chains_data = [
                {"session_id": session_id, "file_name": path}
                for path in new_files
            ]

            # Create chains and refresh to load relationships
            chains = await self.create_bulk(objects_data=chains_data)
            for chain in chains:
                await self.db.refresh(chain)

            logger.info(
                f"Added {len(chains)} new chains to session '{session_id}'. "
                f"Skipped {len(file_names) - len(new_files)} existing chains."
            )
            return chains
        except SQLAlchemyError as e:
            logger.error(f"Database error while selecting chains: {str(e)}")
            raise ChainError("Failed to select chains") from e

    async def get_session_chains(self, session_id: UUID) -> List[Chain]:
        """Get all chains for a specific session."""
        try:
            # Validate session first
            await self._validate_session(session_id)
            query = select(self.model).where(
                self.model.session_id == session_id
            )
            result = await self.db.execute(query)
            chains = list(result.scalars().all())
            logger.info(
                f"Retrieved {len(chains)} configurations for session '{session_id}'"
            )
            return chains
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching chains: {str(e)}")
            raise ChainError("Failed to fetch chains") from e

    async def get_chain_by_id(
        self, *, session_id: UUID, chain_id: UUID
    ) -> Chain:
        """Retrieve a single LCEL chain by ID."""
        return await self._validate_session_chain(
            session_id=session_id, chain_id=chain_id
        )

    async def delete_session_chain(
        self, *, session_id: UUID, chain_id: UUID
    ) -> Chain:
        """Delete a specific chain from a session."""
        try:
            chain = await self._validate_session_chain(
                session_id=session_id, chain_id=chain_id
            )
            await self.delete(db_obj=chain)
            return chain
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting chain: {str(e)}")
            raise ChainError("Failed to delete chain") from e

    async def delete_session_chains(self, session_id: UUID) -> None:
        """Delete all chains for a session."""
        try:
            await self._validate_session(session_id)
            chains = await self.get_session_chains(session_id)
            for chain in chains:
                await self.delete(db_obj=chain)
            logger.info(f"Deleted all chains for session '{session_id}'")
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to delete chains for session '{session_id}': {str(e)}"
            )
            raise ChainError("Failed to delete session chains") from e

    async def invoke_chain_batch(
        self, *, session_id: UUID, chain_id: UUID, config_id: UUID
    ) -> List[Answer]:
        """Invoke chain in batch for all questions in session and save answers."""
        try:
            # Validate chain exists
            chain = await self._validate_session_chain(
                session_id=session_id, chain_id=chain_id
            )

            # Get all questions for the session
            question_service = QuestionService(Question, self.db)
            questions = await question_service.get_session_questions(
                session_id
            )

            if not questions:
                logger.warning(
                    f"No questions found for session '{session_id}'"
                )
                return []

            # Get configuration
            configuration_service = ConfigurationService(
                Configuration, self.db
            )
            config = await configuration_service.get_configuration_by_id(
                session_id=session_id, config_id=config_id
            )

            # Call LangServe batch endpoint
            question_texts = [q.question_text for q in questions]
            async with aiohttp.ClientSession() as session:
                url = f"{os.getenv('LANGSERVE_BASE_URL', 'http://localhost:8001')}/{chain.file_name}/batch"

                payload = {
                    "inputs": question_texts,
                    "config": {"configurable": config.config_values},
                    "kwargs": {},
                }

                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        raise ChainError(
                            f"Chain invocation failed: {await response.text()}"
                        )

                    response_data = await response.json()
                    # Extract answers from output array
                    generated_answers = response_data["output"]

                    if not isinstance(generated_answers, list):
                        raise ChainError(
                            "Invalid response format from LangServe"
                        )

                    # Create AnswerCreate objects mapping questions to their answers
                    answers_data = [
                        AnswerCreate(
                            question_id=question.id,
                            chain_id=chain_id,
                            configuration_id=config_id,
                            generated_answer=answer,
                        )
                        for question, answer in zip(
                            questions, generated_answers
                        )
                    ]

                    logger.critical(
                        f"Answers data: {answers_data}"
                    )  # TODO: Remove this line

                    # Use Answer service to create answers in bulk
                    answer_service = AnswerService(Answer, self.db)
                    answers = await answer_service.create_bulk(
                        objects_data=[
                            answer.model_dump() for answer in answers_data
                        ]
                    )

                    logger.info(
                        f"Created {len(answers)} answers for {len(questions)} questions "
                        f"using chain '{chain_id}' and configuration '{config_id}'"
                    )
                    return answers

        except SQLAlchemyError as e:
            logger.error(f"Database error while invoking chain: {str(e)}")
            raise ChainError("Failed to invoke chain") from e
