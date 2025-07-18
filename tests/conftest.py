"""Test configuration and fixtures."""

from collections.abc import Generator
from typing import Any
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.portia_service import PortiaService


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_portia_service() -> Generator[Mock, None, None]:
    """Mock the PortiaService for testing."""
    with patch.object(PortiaService, "get_instance") as mock_get_instance:
        mock_service = Mock()

        # Make run_query return a coroutine
        async def mock_run_query(*args, **kwargs):  # type: ignore[no-untyped-def] # noqa: ANN002,ANN003,ANN202
            return mock_service.run_query_sync(*args, **kwargs)

        mock_service.run_query = mock_run_query
        mock_get_instance.return_value = mock_service
        yield mock_service


@pytest.fixture
def sample_run_request() -> dict[str, Any]:
    """Sample run request data for testing."""
    return {"query": "What is 2+2?", "tools": ["calculator_tool"]}


@pytest.fixture
def sample_successful_run_result() -> dict[str, Any]:
    """Sample successful run result for testing."""
    return {
        "success": True,
        "result": {
            "value": "4.0",
            "summary": (
                "The query asked for the result of 2+2, and the expression was "
                "evaluated to give the output 4.0."
            ),
        },
        "execution_time": 2.5,
    }


@pytest.fixture
def sample_failed_run_result() -> dict[str, Any]:
    """Sample failed run result for testing."""
    return {"success": False, "error": "Test error message", "execution_time": 1.2}


@pytest.fixture
def sample_available_tools() -> list[str]:
    """Sample available tools for testing."""
    return ["calculator_tool", "weather_tool", "search_tool"]
