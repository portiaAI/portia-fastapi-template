"""Tests for the config module."""

import logging
from unittest.mock import mock_open, patch

import pytest

from app.config import Settings, _get_version_from_pyproject, get_app_config


@pytest.mark.unit
class TestSettings:
    """Test cases for Settings class."""

    def test_settings_defaults(self) -> None:
        """Test Settings with default values."""
        # Clear environment variables to test defaults
        with patch.dict("os.environ", {}, clear=True):
            settings = Settings()

            assert settings.app_name == "Portia FastAPI Example"
            assert settings.debug is False
            assert settings.host == "127.0.0.1"
            assert settings.port == 8000
            assert settings.allowed_domains == ["*"]
            assert settings.portia_config.openai_api_key is None
            assert settings.portia_config.anthropic_api_key is None
            assert settings.portia_config.portia_api_key is None
            assert settings.log_level == "INFO"

    def test_settings_custom_values(self) -> None:
        """Test Settings with custom values."""
        # Clear environment variables to avoid interference
        with patch.dict("os.environ", {}, clear=True):
            custom_settings = Settings(
                app_name="Custom App",
                debug=True,
                host="0.0.0.0",  # noqa: S104
                port=9000,
                allowed_domains=["example.com"],
                log_level="DEBUG",
            )

            assert custom_settings.app_name == "Custom App"
            assert custom_settings.debug is True
            assert custom_settings.host == "0.0.0.0"  # noqa: S104
            assert custom_settings.port == 9000
            assert custom_settings.allowed_domains == ["example.com"]
            assert custom_settings.portia_config.openai_api_key is None
            assert custom_settings.portia_config.anthropic_api_key is None
            assert custom_settings.portia_config.portia_api_key is None
            assert custom_settings.log_level == "DEBUG"

    def test_settings_environment_variables(self) -> None:
        """Test Settings with environment variables."""
        with patch.dict(
            "os.environ",
            {
                "APP_NAME": "Env App",
                "DEBUG": "true",
                "HOST": "192.168.1.1",
                "PORT": "8080",
                "PORTIA_CONFIG__OPENAI_API_KEY": "test_openai_key",
                "PORTIA_CONFIG__ANTHROPIC_API_KEY": "test_anthropic_key",
                "PORTIA_CONFIG__PORTIA_API_KEY": "test_portia_key",
                "LOG_LEVEL": "WARNING",
            },
        ):
            settings = Settings()

            assert settings.app_name == "Env App"
            assert settings.debug is True
            assert settings.host == "192.168.1.1"
            assert settings.port == 8080
            assert settings.portia_config.openai_api_key == "test_openai_key"
            assert settings.portia_config.anthropic_api_key == "test_anthropic_key"
            assert settings.portia_config.portia_api_key == "test_portia_key"
            assert settings.log_level == "WARNING"

    def test_portia_config_conversion(self) -> None:
        """Test converting PortiaConfigSettings to Portia Config."""
        with patch.dict(
            "os.environ",
            {
                "PORTIA_CONFIG__OPENAI_API_KEY": "test_openai_key",
                "PORTIA_CONFIG__ANTHROPIC_API_KEY": "test_anthropic_key",
            },
            clear=True,
        ):
            settings = Settings()
            portia_config = settings.get_portia_config()

            # The actual Config object should have the API keys set
            # Note: Portia Config stores API keys as SecretStr objects
            assert portia_config.openai_api_key.get_secret_value() == "test_openai_key"
            assert portia_config.anthropic_api_key.get_secret_value() == "test_anthropic_key"


@pytest.mark.unit
def test_get_version_from_pyproject() -> None:
    """Test _get_version_from_pyproject function."""
    # Test successful version extraction
    mock_toml_content = b'[project]\nversion = "1.0.0"\n'
    with patch("pathlib.Path.open", mock_open(read_data=mock_toml_content)):
        version = _get_version_from_pyproject()
        assert version == "1.0.0"

    # Test file not found
    with patch("pathlib.Path.open", side_effect=FileNotFoundError):
        version = _get_version_from_pyproject()
        assert version == "unknown"

    # Test missing version key
    mock_toml_content = b'[project]\nname = "test"\n'
    with patch("pathlib.Path.open", mock_open(read_data=mock_toml_content)):
        version = _get_version_from_pyproject()
        assert version == "unknown"


@pytest.mark.unit
def test_get_app_config() -> None:
    """Test get_app_config function."""
    config = get_app_config()

    assert isinstance(config, dict)
    assert config == {}


@pytest.mark.unit
def test_logging_configuration() -> None:
    """Test that logging is configured properly."""
    # Test that logging level is set correctly
    logger = logging.getLogger("app.config")

    # The logger should exist and have proper configuration
    assert logger is not None

    # Test with different log levels
    test_settings = Settings(log_level="DEBUG")
    assert test_settings.log_level == "DEBUG"

    test_settings = Settings(log_level="ERROR")
    assert test_settings.log_level == "ERROR"
