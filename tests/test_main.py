"""Tests for the main FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from app.config import settings


@pytest.mark.unit
def test_root_endpoint(client: TestClient) -> None:
    """Test the root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Welcome to Portia FastAPI Example"
    assert data["version"] == settings.application_version
    assert data["docs_url"] == "/docs"


@pytest.mark.unit
def test_root_endpoint_schema(client: TestClient) -> None:
    """Test the root endpoint response schema."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert "message" in data
    assert "version" in data
    assert "docs_url" in data

    # Check data types
    assert isinstance(data["message"], str)
    assert isinstance(data["version"], str)
    assert isinstance(data["docs_url"], str)


@pytest.mark.unit
def test_docs_endpoint_accessible(client: TestClient) -> None:
    """Test that the docs endpoint is accessible."""
    response = client.get("/docs")

    # Should return HTML content or redirect
    assert response.status_code in [200, 307]


@pytest.mark.unit
def test_openapi_endpoint_accessible(client: TestClient) -> None:
    """Test that the OpenAPI endpoint is accessible."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    data = response.json()

    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == settings.app_name
