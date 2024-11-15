# app/api/deps.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session."""
    async for session in get_session():
        yield session
