from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from langserve import add_routes
from contextlib import asynccontextmanager
from app.db.config import async_engine
from app.models.models import Base
from app.api.endpoints import router

from app.core.logger import get_logger

# from chains.simple_chain import chain


logger = get_logger("ragulator_logger")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application lifecycle events.

    Args:
        app: FastAPI application instance
    """

    logger.info("Starting database initialization...")
    try:
        # Create tables on startup
        async with async_engine.begin() as conn:
            logger.info("Creating database tables...")
            await conn.run_sync(Base.metadata.create_all)
            app.state.db = conn
            logger.info("Database initialization completed")

        logger.info("Application startup completed")
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
    app = FastAPI(
        title="Sample App to test LangServe",
        version="0.0.1",
        description="This app acts as a server for LangServe",
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
    app.include_router(router, prefix="/api/v1")

    return app


app = create_app()
