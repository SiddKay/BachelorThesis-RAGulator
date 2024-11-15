from app.core.logger import get_logger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from app.db.config import AsyncSessionLocal
from time import perf_counter

logger = get_logger(__name__)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session."""

    start_time = perf_counter()
    session_id = id(AsyncSessionLocal)

    async with AsyncSessionLocal() as session:
        logger.debug(f"Creating new database session [id={session_id}]")
        try:
            yield session
            elapsed = perf_counter() - start_time
            logger.debug(
                f"Session completed successfully: [id={session_id}], "
                f"duration={elapsed:.3f}s"
            )
        except Exception as e:
            await session.rollback()
            elapsed = perf_counter() - start_time
            logger.error(
                f"Session [id={session_id}] failed duration={elapsed:.3f}s, "
                f"error={str(e)}",
                exc_info=True,
            )
            raise
        finally:
            await session.close()
            logger.debug(f"Session closed [id={session_id}]")
