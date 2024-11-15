import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

# Database URL configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ragulator")


PG_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

# SQLAlchemy engine configuration
async_engine = create_async_engine(
    PG_DATABASE_URL,
    echo=True,  # TODO: Set to False to disable SQL query logging overhead
    pool_size=32,  # Increased for better concurrency
    max_overflow=64,  # Double pool_size for burst handling
    pool_timeout=10,  # Faster timeout for local development
    pool_recycle=300,  # 5 minutes - Docker containers are ephemeral
    pool_pre_ping=True,  # Verify connections before use
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (better for API)
    autocommit=False,  # Explicit transaction management
    autoflush=True,  # Auto-flush for better cache management
    twophase=False,  # No distributed transactions(for multiple databases) needed
    future=True,  # Use future SQLAlchemy features
)
