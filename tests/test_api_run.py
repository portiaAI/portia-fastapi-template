"""Tests for the run API endpoint."""

from typing import Any
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.exceptions import InvalidToolsError


@pytest.mark.unit
def test_run_query_success(
    client: TestClient,
    mock_portia_service: Mock,
    sample_run_request: dict[str, Any],
    sample_successful_run_result: dict[str, Any],
) -> None:
    """Test successful query execution."""
    mock_portia_service.run_query_sync.return_value = sample_successful_run_result

    response = client.post("/run", json=sample_run_request)

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["result"]["value"] == "4.0"
    assert "summary" in data["result"]
    assert data["execution_time"] == 2.5
    assert data["error"] is None

    # Verify the service was called with correct parameters
    mock_portia_service.run_query_sync.assert_called_once_with(
        query=sample_run_request["query"], tools=sample_run_request["tools"]
    )


@pytest.mark.unit
def test_run_query_failure(
    client: TestClient,
    mock_portia_service: Mock,
    sample_run_request: dict[str, Any],
    sample_failed_run_result: dict[str, Any],
) -> None:
    """Test failed query execution."""
    mock_portia_service.run_query_sync.return_value = sample_failed_run_result

    response = client.post("/run", json=sample_run_request)

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Test error message"
    assert data["execution_time"] == 1.2
    assert data["result"] is None


@pytest.mark.unit
def test_run_query_invalid_tools(
    client: TestClient,
    mock_portia_service: Mock,
    sample_run_request: dict[str, Any],
) -> None:
    """Test query execution with invalid tools."""
    invalid_tools = ["invalid_tool"]
    available_tools = ["calculator_tool", "weather_tool"]

    mock_portia_service.run_query_sync.side_effect = InvalidToolsError(
        invalid_tools=invalid_tools, available_tools=available_tools
    )

    response = client.post("/run", json=sample_run_request)

    assert response.status_code == 400
    data = response.json()

    assert data["detail"]["error"] == "Invalid tools requested"
    assert data["detail"]["invalid_tools"] == invalid_tools
    assert data["detail"]["available_tools"] == available_tools


@pytest.mark.unit
def test_run_query_unexpected_error(
    client: TestClient,
    mock_portia_service: Mock,
    sample_run_request: dict[str, Any],
) -> None:
    """Test query execution with unexpected error."""
    mock_portia_service.run_query_sync.side_effect = Exception("Unexpected error")

    response = client.post("/run", json=sample_run_request)

    assert response.status_code == 500
    data = response.json()

    assert "Internal server error" in data["detail"]


@pytest.mark.unit
def test_run_query_invalid_request_empty_query(client: TestClient) -> None:
    """Test run query with empty query."""
    invalid_request = {"query": "", "tools": ["calculator_tool"]}

    response = client.post("/run", json=invalid_request)

    assert response.status_code == 422


@pytest.mark.unit
def test_run_query_invalid_request_missing_query(client: TestClient) -> None:
    """Test run query with missing query."""
    invalid_request = {"tools": ["calculator_tool"]}

    response = client.post("/run", json=invalid_request)

    assert response.status_code == 422


@pytest.mark.unit
def test_run_query_invalid_request_missing_tools(client: TestClient) -> None:
    """Test run query with missing tools."""
    invalid_request = {"query": "What is 2+2?"}

    response = client.post("/run", json=invalid_request)

    assert response.status_code == 422


@pytest.mark.unit
def test_get_available_tools_success(
    client: TestClient,
    mock_portia_service: Mock,
    sample_available_tools: list[str],
) -> None:
    """Test successful retrieval of available tools."""
    mock_portia_service.available_tool_ids.return_value = sample_available_tools

    response = client.get("/tools")

    assert response.status_code == 200
    data = response.json()

    assert data == sample_available_tools
    mock_portia_service.available_tool_ids.assert_called_once()


@pytest.mark.unit
def test_get_available_tools_error(
    client: TestClient,
    mock_portia_service: Mock,
) -> None:
    """Test error when retrieving available tools."""
    mock_portia_service.available_tool_ids.side_effect = Exception("Service error")

    response = client.get("/tools")

    assert response.status_code == 500
    data = response.json()

    assert "Failed to get available tools" in data["detail"]
