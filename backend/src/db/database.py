import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""

    pass


class DatabaseError(Exception):
    """Custom exception for database errors"""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class Database:
    def __init__(self):
        self.engine = None
        self.async_session_maker = None

    async def connect(self) -> None:
        """Initialize database engine and session maker"""
        try:
            DATABASE_URL = (
                f"postgresql+asyncpg://"
                f"{os.getenv('POSTGRES_USER', 'postgres')}:"
                f"{os.getenv('POSTGRES_PASSWORD', '')}@"
                f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
                f"{os.getenv('POSTGRES_PORT', '5432')}/"
                f"{os.getenv('POSTGRES_DB', 'ragulator')}"
            )

            self.engine = create_async_engine(
                DATABASE_URL,
                pool_size=5,
                max_overflow=10,
                echo=False,
            )

            self.async_session_maker = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
            )

        except Exception as e:
            raise DatabaseError(f"Failed to initialize database: {str(e)}", e)

    async def disconnect(self) -> None:
        """Close database connections"""
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.async_session_maker = None

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session with automatic cleanup"""
        if not self.async_session_maker:
            await self.connect()

        session = self.async_session_maker()
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Database session error: {str(e)}", e)
        except Exception as e:
            await session.rollback()
            raise DatabaseError(f"Unexpected error: {str(e)}", e)
        finally:
            await session.close()


# Create database instance
db = Database()
