from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.models import Base
from app.db.config import async_engine
from app.api.v1.endpoints import api_router
from app.core.logger import setup_logging, get_logger


logger = get_logger("ragulator_logger")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages application lifecycle events."""

    # Setup logging
    setup_logging(log_file="logs/ragulator_log")

    logger.info("Starting application initialization...")
    try:
        # Initialize database
        async with async_engine.begin() as conn:
            logger.info("Creating database tables...")
            await conn.run_sync(Base.metadata.create_all)
            app.state.db = conn
            logger.info("Database initialization completed")
        yield

    except Exception as e:
        logger.error(
            f"Failed to initialize application: {str(e)}", exc_info=True
        )
        raise

    finally:
        # Clean up resources on shutdown
        logger.info("Shutting down application...")
        if hasattr(app.state, "db"):
            await app.state.db.close()
        await async_engine.dispose()
        logger.info("Application shutdown completed")


def create_app() -> FastAPI:
    """Create and configure the main FastAPI application."""
    app = FastAPI(
        title="RAGulator API",
        version="0.0.1",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Add routes
    app.include_router(api_router, prefix="/v1")

    return app


app = create_app()
