from app.core.logger import get_logger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from app.db.config import AsyncSessionLocal
from time import perf_counter

logger = get_logger(__name__)


async def get_session() -> AsyncGenerator[AsyncSession, None]:

    start_time = perf_counter()
    session_id = id(AsyncSessionLocal)

    logger.debug(f"Creating database session [id={session_id}]")

    async with AsyncSessionLocal() as session:
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
                f"Session failed [id={session_id}] duration={elapsed:.3f}s "
                f"error={str(e)}",
                exc_info=True,
            )
            raise
        finally:
            await session.close()
            logger.debug(f"Session closed [id={session_id}]")
