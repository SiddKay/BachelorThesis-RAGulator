from typing import List, Type, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
import os

from app.core.logger import get_logger
from app.models.session import Session
from app.models.chain import Chain
from app.models.configuration import Configuration
from app.services.base import BaseService
from app.schemas.configuration import (
    ConfigurationCreate,
    ConfigurationUpdate,
    ConfigSchema,
)
from app.services.exceptions import (
    SessionNotFoundError,
    ConfigurationError,
    ConfigurationNotFoundError,
    ChainNotFoundError,
)

logger = get_logger(__name__)


class ConfigurationService(BaseService[Configuration]):
    def __init__(self, model: Type[Configuration], db: AsyncSession):
        super().__init__(model, db)
        self.session_model = Session
        self.chain_model = Chain
        self.langserve_base_url = os.getenv(
            "LANGSERVE_BASE_URL", "http://localhost:8001"
        )

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

    async def _validate_chain(
        self,
        *,
        session_id: UUID,
        chain_id: UUID,
    ) -> Chain:
        """Validate if the chain exists."""
        try:
            await self._validate_session(session_id)

            query = select(self.chain_model).where(
                self.chain_model.id == chain_id
            )
            result = await self.db.execute(query)
            chain = result.scalar_one_or_none()
            if not chain:
                raise ChainNotFoundError(
                    f"Chain with id '{chain_id}' not found"
                )
            return chain
        except SQLAlchemyError as e:
            logger.error(f"Database error while validating chain: {str(e)}")
            raise ConfigurationError("Failed to validate chain") from e

    async def _fetch_config_schema(
        self, chain_file_name: str
    ) -> Dict[str, Any]:
        """
        Fetch configuration schema from LangServe endpoint using aiohttp.

        Args:
            chain_file_name: Name of the chain file

        Returns:
            Dict[str, Any]: Configuration schema for the chain

        Raises:
            ConfigurationError: If fetching schema fails
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{self.langserve_base_url}/{chain_file_name}/config_schema"
                async with session.get(url) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise ConfigurationError(
                            f"Failed to fetch config schema for the url {url}: {error_text}"
                        )
                    return await response.json()

            except aiohttp.ClientError as e:
                logger.error(
                    f"Network error while fetching config schema: {str(e)}"
                )
                raise ConfigurationError(
                    f"Failed to connect to LangServe endpoint: {str(e)}"
                )
            except Exception as e:
                logger.error(
                    f"Unexpected error fetching config schema: {str(e)}"
                )
                raise ConfigurationError(
                    f"Unexpected error fetching config schema: {str(e)}"
                )

    async def get_chain_schema(
        self, *, session_id: UUID, chain_id: UUID
    ) -> ConfigSchema:
        """Fetch configuration schema from LangServe endpoint."""
        try:
            chain = await self._validate_chain(
                session_id=session_id, chain_id=chain_id
            )

            schema = await self._fetch_config_schema(chain.file_name)
            return ConfigSchema(config_schema=schema)
        except (ChainNotFoundError, SessionNotFoundError) as e:
            raise e
        except Exception as e:
            logger.error(f"Failed to fetch the chain config schema: {str(e)}")
            raise ConfigurationError(
                f"Failed to fetch config schema for chain {chain.file_name}"
            )

    async def create_configuration(
        self,
        *,
        session_id: UUID,
        chain_id: UUID,
        data: ConfigurationCreate,
    ) -> Configuration:
        """Create a new configuration within a session."""
        try:
            # Validate session first
            await self._validate_session(session_id)
            config_data = data.model_dump(exclude_unset=True)
            config_data["session_id"] = session_id
            config_data["chain_id"] = chain_id

            config = await self.create(obj_data=config_data)
            logger.info(
                f"Created configuration for chain '{chain_id}' in session '{session_id}'"
            )
            return config
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while creating configuration: {str(e)}"
            )
            raise ConfigurationError("Failed to create configuration") from e

    async def get_chain_configurations(
        self, *, session_id: UUID, chain_id: UUID
    ) -> List[Configuration]:
        """Get all configurations for a chain."""
        try:
            # Validate session first
            await self._validate_chain(
                session_id=session_id, chain_id=chain_id
            )

            query = select(self.model).where(
                self.model.session_id == session_id,
                self.model.chain_id == chain_id,
            )
            result = await self.db.execute(query)
            configs = list(result.scalars().all())
            logger.info(
                f"Retrieved {len(configs)} configurations for chain '{chain_id}'"
            )
            return configs
        except SQLAlchemyError as e:
            logger.error(f"Failed to fetch configurations: {str(e)}")
            raise ConfigurationError("Failed to fetch configurations") from e

    async def get_configuration_by_id(
        self, *, session_id: UUID, config_id: UUID
    ) -> Configuration:
        """Retrieve a single configuration by ID."""
        return await self._validate_session_configuration(
            session_id=session_id, config_id=config_id
        )

    async def update_configuration(
        self,
        *,
        session_id: UUID,
        config_id: UUID,
        chain_id: UUID,
        data: ConfigurationUpdate,
    ) -> Configuration:
        """Update an existing configuration."""
        try:
            _ = await self._validate_chain(
                session_id=session_id, chain_id=chain_id
            )
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
