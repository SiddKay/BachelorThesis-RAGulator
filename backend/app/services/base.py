# app/services/base.py
from uuid import UUID
from time import perf_counter
from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic, Optional, List, Type, Any
from sqlalchemy.exc import SQLAlchemyError
from app.models.base import BaseModel
from app.core.logger import get_logger

ModelType = TypeVar("ModelType", bound=BaseModel)

logger = get_logger(__name__)


class BaseService(Generic[ModelType]):
    """Base service class for database operations."""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, *, obj_data: dict[str, Any]) -> ModelType:
        """Create a new object."""
        start_time = perf_counter()
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)

        try:
            await self.db.commit()

            # Logging the time taken to create the object
            elapsed = perf_counter() - start_time
            logger.info(
                f"Created `{self.model.__name__}` in {elapsed:.3f}s",
            )

            return db_obj
        except SQLAlchemyError as e:
            await self.db.rollback()

            logger.error(
                f"Failed to create {self.model.__name__}: {str(e)}",
                exc_info=True,
            )
            raise

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_at",
        ascending: bool = False,
    ) -> List[ModelType]:
        """Get multiple objects with optional pagination and sorting."""
        start_time = perf_counter()
        try:
            try:
                sort_column = getattr(self.model, order_by)
                logger.info(f"Sorting the column by order '{sort_column}'.")
            except AttributeError:
                logger.warning(
                    f"Invalid sort column '{order_by}', falling back to 'created_at'"
                )
                sort_column = self.model.created_at

            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(asc(sort_column) if ascending else desc(sort_column))
            )
            result = await self.db.execute(query)
            items = list(result.scalars().all())

            # Logging the time taken to fetch the objects
            elapsed = perf_counter() - start_time
            logger.info(
                f"Retrieved {len(items)} {self.model.__name__}s in {elapsed:.3f}s"
            )

            return items
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to fetch {self.model.__name__} objects: {str(e)}",
                exc_info=True,
            )
            raise

    async def get(self, id: UUID) -> Optional[ModelType]:
        """Get a single object by ID."""
        try:
            result = await self.db.execute(
                select(self.model).where(self.model.id == id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get {self.model.__name__} with id {id}: {str(e)}",
                exc_info=True,
            )
            raise

    async def update(
        self, *, db_obj: ModelType, obj_data: dict[str, Any]
    ) -> ModelType:
        """Update an object by ID."""
        start_time = perf_counter()
        try:
            for field, value in obj_data.items():
                setattr(db_obj, field, value)
            await self.db.commit()
            await self.db.refresh(db_obj)

            # Logging the time taken to update the object
            elapsed = perf_counter() - start_time
            logger.info(
                f"Updated `{self.model.__name__}` in {elapsed:.3f}s",
            )

            return db_obj
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                f"Failed to update {self.model.__name__}: {str(e)}",
                exc_info=True,
            )
            raise

    async def delete(self, *, db_obj: ModelType) -> None:
        """Delete an object by ID."""
        start_time = perf_counter()
        try:
            await self.db.delete(db_obj)
            await self.db.commit()

            # Logging the time taken to delete the object
            elapsed = perf_counter() - start_time
            logger.warning(
                f"Deleted `{self.model.__name__}` in {elapsed:.3f}s",
            )

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                f"Failed to delete {self.model.__name__}: {str(e)}",
                exc_info=True,
            )
            raise
