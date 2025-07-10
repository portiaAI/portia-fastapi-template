"""Tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.health import HealthResponse
from app.schemas.run import RunRequest, RunResponse


@pytest.mark.unit
class TestHealthResponse:
    """Test cases for HealthResponse schema."""

    def test_health_response_valid(self) -> None:
        """Test valid HealthResponse creation."""
        response = HealthResponse(status="healthy", version="1.0.0")

        assert response.status == "healthy"
        assert response.version == "1.0.0"

    def test_health_response_missing_status(self) -> None:
        """Test HealthResponse with missing status."""
        with pytest.raises(ValidationError) as exc_info:
            HealthResponse(version="1.0.0")  # type: ignore[call-arg]

        assert "status" in str(exc_info.value)

    def test_health_response_missing_version(self) -> None:
        """Test HealthResponse with missing version."""
        with pytest.raises(ValidationError) as exc_info:
            HealthResponse(status="healthy")  # type: ignore[call-arg]

        assert "version" in str(exc_info.value)


@pytest.mark.unit
class TestRunRequest:
    """Test cases for RunRequest schema."""

    def test_run_request_valid(self) -> None:
        """Test valid RunRequest creation."""
        request = RunRequest(query="What is 2+2?", tools=["calculator_tool"])

        assert request.query == "What is 2+2?"
        assert request.tools == ["calculator_tool"]

    def test_run_request_empty_query(self) -> None:
        """Test RunRequest with empty query."""
        with pytest.raises(ValidationError) as exc_info:
            RunRequest(query="", tools=["calculator_tool"])

        assert "at least 1 character" in str(exc_info.value)

    def test_run_request_missing_query(self) -> None:
        """Test RunRequest with missing query."""
        with pytest.raises(ValidationError) as exc_info:
            RunRequest(tools=["calculator_tool"])  # type: ignore[call-arg]

        assert "query" in str(exc_info.value)

    def test_run_request_missing_tools(self) -> None:
        """Test RunRequest with missing tools."""
        with pytest.raises(ValidationError) as exc_info:
            RunRequest(query="What is 2+2?")  # type: ignore[call-arg]

        assert "tools" in str(exc_info.value)

    def test_run_request_multiple_tools(self) -> None:
        """Test RunRequest with multiple tools."""
        request = RunRequest(
            query="What is the weather and 2+2?", tools=["calculator_tool", "weather_tool"]
        )

        assert len(request.tools) == 2
        assert "calculator_tool" in request.tools
        assert "weather_tool" in request.tools

    def test_run_request_empty_tools_list(self) -> None:
        """Test RunRequest with empty tools list."""
        request = RunRequest(query="What is 2+2?", tools=[])

        assert request.tools == []


@pytest.mark.unit
class TestRunResponse:
    """Test cases for RunResponse schema."""

    def test_run_response_success(self) -> None:
        """Test successful RunResponse creation."""
        response = RunResponse(success=True, result={"value": "4.0"}, execution_time=2.5)

        assert response.success is True
        assert response.result == {"value": "4.0"}
        assert response.execution_time == 2.5
        assert response.error is None

    def test_run_response_failure(self) -> None:
        """Test failed RunResponse creation."""
        response = RunResponse(success=False, error="Test error message", execution_time=1.2)

        assert response.success is False
        assert response.error == "Test error message"
        assert response.execution_time == 1.2
        assert response.result is None

    def test_run_response_minimal(self) -> None:
        """Test RunResponse with minimal required fields."""
        response = RunResponse(success=True)

        assert response.success is True
        assert response.result is None
        assert response.error is None
        assert response.execution_time is None

    def test_run_response_missing_success(self) -> None:
        """Test RunResponse with missing success field."""
        with pytest.raises(ValidationError) as exc_info:
            RunResponse(result={"value": "4.0"})  # type: ignore[call-arg]

        assert "success" in str(exc_info.value)

    def test_run_response_complex_result(self) -> None:
        """Test RunResponse with complex result data."""
        complex_result = {
            "value": "4.0",
            "summary": "The calculation was successful",
            "details": {"operation": "addition", "operands": [2, 2]},
        }

        response = RunResponse(success=True, result=complex_result, execution_time=3.7)

        assert response.result == complex_result
        assert response.result["details"]["operation"] == "addition"
