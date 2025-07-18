"""Main FastAPI application."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.run import router as run_router
from app.config import get_app_config, settings
from app.services.portia_service import PortiaService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Async context manager for application lifespan.

    Handles startup and shutdown events.
    """
    logger.info("Starting up FastAPI application and initializing Portia service")
    # Initialize Portia service singleton
    PortiaService()

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application")


app_config = get_app_config()

# Create FastAPI app with lifespan
app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    version=settings.application_version,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_domains,
    allow_credentials=True,
)
# Include API routes
app.include_router(
    run_router,
    tags=["run"],
)

app.include_router(
    health_router,
    tags=["health"],
)


# Root endpoint
@app.get("/", summary="Root endpoint", description="Welcome message")
async def root() -> dict[str, str]:
    """Root endpoint that returns a welcome message."""
    return {
        "message": "Welcome to Portia FastAPI Example",
        "version": settings.application_version,
        "docs_url": "/docs",
    }
