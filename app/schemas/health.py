"""Pydantic schemas for the /health endpoint."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for health checks."""

    status: str = Field(..., description="Application status")
    version: str = Field(..., description="Application version")
    model_config = {"json_schema_extra": {"examples": [{"status": "healthy", "version": "0.1.0"}]}}
