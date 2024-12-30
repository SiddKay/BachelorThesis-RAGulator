from typing import List
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.core.logger import get_logger
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate
from app.services.base import BaseService
from app.services.exceptions import SessionError, SessionNotFoundError

logger = get_logger(__name__)


class SessionService(BaseService[Session]):
    async def create_session(self, data: SessionCreate) -> Session:
        """Create a new evaluation session."""
        try:
            session_data = data.model_dump(exclude_unset=True)
            session = await self.create(obj_data=session_data)
            logger.info(f"Created session: '{session.name}'")
            return session
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating session: {str(e)}")
            raise SessionError("Failed to create session") from e

    async def get_sessions(
        self, skip: int = 0, limit: int = 100
    ) -> List[Session]:
        """Retrieve a list of evaluation sessions."""
        try:
            sessions = await self.get_multi(
                skip=skip, limit=limit, order_by="last_modified"
            )

            logger.info(f"Retrieved {len(sessions)} sessions")

            return sessions
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching sessions: {str(e)}")
            raise SessionError("Failed to fetch sessions") from e

    async def get_session_by_id(self, session_id: UUID) -> Session:
        """Retrieve a single evaluation session by ID."""
        try:
            session = await self.get(session_id)
            if not session:
                raise SessionNotFoundError(f"Session '{session_id}' not found")
            return session
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching session: {str(e)}")
            raise SessionError("Failed to fetch session") from e

    async def update_session(
        self, session_id: UUID, data: SessionUpdate
    ) -> Session:
        """Update an existing evaluation session."""
        try:
            session = await self.get(session_id)
            if not session:
                raise SessionNotFoundError(f"Session '{session_id}' not found")

            update_data = data.model_dump(exclude_unset=True)
            updated_session = await self.update(
                db_obj=session, obj_data=update_data
            )
            return updated_session
        except SQLAlchemyError as e:
            logger.error(f"Database error while updating session: {str(e)}")
            raise SessionError("Failed to update session") from e

    async def delete_session(self, session_id: UUID) -> Session:
        """Delete an existing evaluation session."""
        try:
            session = await self.get(session_id)
            if not session:
                raise SessionNotFoundError(f"Session '{session_id}' not found")

            await self.delete(db_obj=session)
            return session
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting session: {str(e)}")
            raise SessionError("Failed to delete session") from e
