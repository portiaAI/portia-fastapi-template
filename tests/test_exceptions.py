"""Tests for custom exceptions."""

import pytest

from app.exceptions import InvalidToolsError


@pytest.mark.unit
class TestInvalidToolsError:
    """Test cases for InvalidToolsError exception."""

    def test_invalid_tools_error_creation(self) -> None:
        """Test InvalidToolsError creation with valid parameters."""
        invalid_tools = ["invalid_tool1", "invalid_tool2"]
        available_tools = ["valid_tool1", "valid_tool2", "valid_tool3"]

        error = InvalidToolsError(invalid_tools, available_tools)

        assert error.invalid_tools == invalid_tools
        assert error.available_tools == available_tools
        assert "invalid_tool1" in str(error)
        assert "invalid_tool2" in str(error)
        assert "valid_tool1" in str(error)

    def test_invalid_tools_error_message(self) -> None:
        """Test InvalidToolsError message format."""
        invalid_tools = ["tool1"]
        available_tools = ["tool2", "tool3"]

        error = InvalidToolsError(invalid_tools, available_tools)
        message = str(error)

        assert "The following tools are not available: tool1" in message
        assert "Available tools: tool2, tool3" in message

    def test_invalid_tools_error_empty_invalid_tools(self) -> None:
        """Test InvalidToolsError with empty invalid tools list."""
        invalid_tools: list[str] = []
        available_tools = ["tool1", "tool2"]

        error = InvalidToolsError(invalid_tools, available_tools)
        message = str(error)

        assert "The following tools are not available: " in message
        assert "Available tools: tool1, tool2" in message

    def test_invalid_tools_error_empty_available_tools(self) -> None:
        """Test InvalidToolsError with empty available tools list."""
        invalid_tools = ["tool1"]
        available_tools: list[str] = []

        error = InvalidToolsError(invalid_tools, available_tools)
        message = str(error)

        assert "The following tools are not available: tool1" in message
        assert "Available tools: " in message

    def test_invalid_tools_error_single_tool(self) -> None:
        """Test InvalidToolsError with single invalid tool."""
        invalid_tools = ["single_tool"]
        available_tools = ["available_tool"]

        error = InvalidToolsError(invalid_tools, available_tools)

        assert error.invalid_tools == ["single_tool"]
        assert error.available_tools == ["available_tool"]

    def test_invalid_tools_error_inheritance(self) -> None:
        """Test that InvalidToolsError inherits from Exception."""
        invalid_tools = ["tool1"]
        available_tools = ["tool2"]

        error = InvalidToolsError(invalid_tools, available_tools)

        assert isinstance(error, Exception)
        assert isinstance(error, InvalidToolsError)
