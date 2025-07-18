"""Tests for the health API endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.config import settings


@pytest.mark.unit
def test_health_check_success(client: TestClient) -> None:
    """Test successful health check."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["version"] == settings.application_version


@pytest.mark.unit
def test_health_check_response_schema(client: TestClient) -> None:
    """Test health check response schema."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert "status" in data
    assert "version" in data

    # Check data types
    assert isinstance(data["status"], str)
    assert isinstance(data["version"], str)
