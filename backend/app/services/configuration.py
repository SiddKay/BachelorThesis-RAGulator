from typing import List, Type
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.session import Session
from app.models.configuration import Configuration
from app.services.base import BaseService
from app.schemas.configuration import ConfigurationCreate, ConfigurationUpdate
from app.services.exceptions import (
    SessionNotFoundError,
    ConfigurationError,
    ConfigurationNotFoundError,
)

logger = get_logger(__name__)


class ConfigurationService(BaseService[Configuration]):
    def __init__(self, model: Type[Configuration], db: AsyncSession):
        super().__init__(model, db)
        self.session_model = Session

    async def _validate_session(self, session_id: UUID) -> bool:
        """Validate if the queried session exists."""
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
            raise ConfigurationError("Failed to validate session") from e

    async def _validate_session_configuration(
        self, *, session_id: UUID, config_id: UUID
    ) -> Configuration:
        """Validate that the queried configuration belongs to the queried session."""
        try:
            await self._validate_session(session_id)
            config = await self.get(config_id)

            if not config:
                raise ConfigurationNotFoundError(
                    f"Configuration '{config_id}' not found"
                )

            if config.session_id != session_id:
                raise ConfigurationNotFoundError(
                    f"Configuration '{config_id}' not found in session '{session_id}'"
                )

            return config
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while validating configuration: {str(e)}"
            )
            raise ConfigurationError("Failed to validate configuration") from e

    async def create_configuration(
        self, *, session_id: UUID, data: ConfigurationCreate
    ) -> Configuration:
        """Create a new configuration within a session."""
        try:
            # Validate session first
            await self._validate_session(session_id)
            config_data = data.model_dump(exclude_unset=True)
            config_data["session_id"] = session_id
            config = await self.create(obj_data=config_data)
            logger.info(f"Created configuration in session '{session_id}'")
            return config
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while creating configuration: {str(e)}"
            )
            raise ConfigurationError("Failed to create configuration") from e

    async def get_session_configurations(
        self, session_id: UUID
    ) -> List[Configuration]:
        """Get all configurations for a specific session."""
        try:
            # Validate session first
            await self._validate_session(session_id)
            query = select(self.model).where(
                self.model.session_id == session_id
            )
            result = await self.db.execute(query)
            configs = list(result.scalars().all())
            logger.info(
                f"Retrieved {len(configs)} configurations for session '{session_id}'"
            )
            return configs
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while fetching configurations: {str(e)}"
            )
            raise ConfigurationError("Failed to fetch configurations") from e

    async def get_configuration_by_id(
        self, *, session_id: UUID, config_id: UUID
    ) -> Configuration:
        """Retrieve a single configuration by ID."""
        return await self._validate_session_configuration(
            session_id=session_id, config_id=config_id
        )

    async def update_configuration(
        self, *, session_id: UUID, config_id: UUID, data: ConfigurationUpdate
    ) -> Configuration:
        """Update an existing configuration."""
        try:
            config = await self._validate_session_configuration(
                session_id=session_id, config_id=config_id
            )
            update_data = data.model_dump(exclude_unset=True)
            return await self.update(db_obj=config, obj_data=update_data)
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while updating configuration: {str(e)}"
            )
            raise ConfigurationError("Failed to update configuration") from e

    async def delete_configuration(
        self, *, session_id: UUID, config_id: UUID
    ) -> Configuration:
        """Delete a specific configuration from a session."""
        try:
            config = await self._validate_session_configuration(
                session_id=session_id, config_id=config_id
            )
            await self.delete(db_obj=config)
            logger.warning(
                f"Deleted configuration '{config_id}' from session '{session_id}'"
            )
            return config
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while deleting configuration: {str(e)}"
            )
            raise ConfigurationError("Failed to delete configuration") from e
