"""API endpoints for the /run functionality."""

import logging

from fastapi import APIRouter, status

from app.config import settings
from app.schemas.health import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the health of the application and Portia SDK",
)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns the current status of the application and Portia SDK.
    """
    return HealthResponse(
        status="healthy",
        version=settings.application_version,
    )
