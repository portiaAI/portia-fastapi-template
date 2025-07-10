"""Tests for the services layer."""

from unittest.mock import Mock, patch

import pytest

from app.exceptions import InvalidToolsError
from app.services.portia_service import PortiaService


@pytest.mark.unit
class TestPortiaService:
    """Test cases for PortiaService."""

    def setup_method(self) -> None:
        """Reset the singleton instance before each test."""
        PortiaService._instance = None  # noqa: SLF001

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    def test_singleton_behavior(
        self,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test that PortiaService follows singleton pattern."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = None

        mock_tool = Mock()
        mock_tool.id = "test_tool"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool]
        _mock_portia_registry.return_value.get_tools.return_value = []

        service1 = PortiaService()
        service2 = PortiaService()
        service3 = PortiaService.get_instance()

        assert service1 is service2
        assert service2 is service3
        assert service1 is service3

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    def test_initialization(
        self,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test PortiaService initialization."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = "test_key"

        mock_tool = Mock()
        mock_tool.id = "test_tool"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool]
        _mock_portia_registry.return_value.get_tools.return_value = []

        service = PortiaService()

        assert service._config == mock_config_instance  # noqa: SLF001
        assert hasattr(service, "_initialized")
        assert service._initialized is True  # noqa: SLF001

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    def test_available_tool_ids(
        self,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test getting available tool IDs."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = None

        mock_tool1 = Mock()
        mock_tool1.id = "tool1"
        mock_tool2 = Mock()
        mock_tool2.id = "tool2"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool1, mock_tool2]

        service = PortiaService()
        tool_ids = service.available_tool_ids()

        assert len(tool_ids) == 2
        assert "tool1" in tool_ids
        assert "tool2" in tool_ids

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    @patch("app.services.portia_service.Portia")
    def test_get_portia_instance_valid_tools(
        self,
        mock_portia: Mock,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test getting Portia instance with valid tools."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = None

        mock_tool = Mock()
        mock_tool.id = "test_tool"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool]

        mock_portia_instance = Mock()
        mock_portia.return_value = mock_portia_instance

        service = PortiaService()
        tools = {"test_tool"}

        result = service._get_portia_instance(tools)  # noqa: SLF001

        assert result == mock_portia_instance
        mock_portia.assert_called_once_with(
            config=mock_config_instance, tools=[mock_tool], execution_hooks=None
        )

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    def test_get_portia_instance_invalid_tools(
        self,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test getting Portia instance with invalid tools."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = None

        mock_tool = Mock()
        mock_tool.id = "valid_tool"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool]

        service = PortiaService()
        invalid_tools = {"invalid_tool"}

        with pytest.raises(InvalidToolsError) as exc_info:
            service._get_portia_instance(invalid_tools)  # noqa: SLF001

        assert exc_info.value.invalid_tools == ["invalid_tool"]
        assert exc_info.value.available_tools == ["valid_tool"]

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    @patch("app.services.portia_service.Portia")
    @pytest.mark.asyncio
    async def test_run_query_success(
        self,
        mock_portia: Mock,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test successful query execution."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = None

        mock_tool = Mock()
        mock_tool.id = "test_tool"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool]

        mock_plan_run = Mock()
        mock_plan_run.outputs.final_output = {"result": "success"}
        mock_portia_instance = Mock()
        mock_portia_instance.run.return_value = mock_plan_run
        mock_portia.return_value = mock_portia_instance

        service = PortiaService()

        with patch("time.time", side_effect=[0.0, 2.5, 2.5, 2.5, 2.5]):
            result = await service.run_query("test query", ["test_tool"])

        assert result["success"] is True
        assert result["result"] == {"result": "success"}
        assert isinstance(result["execution_time"], (int, float))

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    @patch("app.services.portia_service.Portia")
    @pytest.mark.asyncio
    async def test_run_query_failure(
        self,
        mock_portia: Mock,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test query execution failure."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = None

        mock_tool = Mock()
        mock_tool.id = "test_tool"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool]

        mock_portia_instance = Mock()
        mock_portia_instance.run.side_effect = Exception("Test error")
        mock_portia.return_value = mock_portia_instance

        service = PortiaService()

        with patch("time.time", side_effect=[0.0, 1.5, 1.5, 1.5, 1.5]):
            result = await service.run_query("test query", ["test_tool"])

        assert result["success"] is False
        assert result["error"] == "Test error"
        assert isinstance(result["execution_time"], (int, float))

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    @pytest.mark.asyncio
    async def test_run_query_invalid_tools(
        self,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test query execution with invalid tools."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = None

        mock_tool = Mock()
        mock_tool.id = "valid_tool"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool]

        service = PortiaService()

        with pytest.raises(InvalidToolsError):
            await service.run_query("test query", ["invalid_tool"])

    @patch("app.services.portia_service.Config")
    @patch("app.services.portia_service.DefaultToolRegistry")
    @patch("app.services.portia_service.PortiaToolRegistry")
    @patch("app.services.portia_service.Portia")
    def test_reuse_portia_instance(
        self,
        mock_portia: Mock,
        _mock_portia_registry: Mock,  # noqa: PT019
        mock_default_registry: Mock,
        mock_config: Mock,
    ) -> None:
        """Test that Portia instances are reused for the same tool set."""
        # Setup mocks
        mock_config_instance = Mock()
        mock_config.from_default.return_value = mock_config_instance
        mock_config_instance.portia_api_key = None

        mock_tool = Mock()
        mock_tool.id = "test_tool"
        mock_default_registry.return_value.get_tools.return_value = [mock_tool]

        mock_portia_instance = Mock()
        mock_portia.return_value = mock_portia_instance

        service = PortiaService()
        tools = {"test_tool"}

        # First call should create instance
        result1 = service._get_portia_instance(tools)  # noqa: SLF001
        # Second call should reuse instance
        result2 = service._get_portia_instance(tools)  # noqa: SLF001

        assert result1 is result2
        # Portia should only be called once
        mock_portia.assert_called_once()
