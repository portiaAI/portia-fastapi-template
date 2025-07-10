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
            assert settings.portia_api_key is None
            assert settings.openai_api_key is None
            assert settings.anthropic_api_key is None
            assert settings.log_level == "INFO"

    def test_settings_custom_values(self) -> None:
        """Test Settings with custom values."""
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
                "PORTIA_API_KEY": "test_key",
                "LOG_LEVEL": "WARNING",
            },
        ):
            settings = Settings()

            assert settings.app_name == "Env App"
            assert settings.debug is True
            assert settings.host == "192.168.1.1"
            assert settings.port == 8080
            assert settings.portia_api_key == "test_key"
            assert settings.log_level == "WARNING"


@pytest.mark.unit
class TestGetVersionFromPyproject:
    """Test cases for _get_version_from_pyproject function."""

    def test_get_version_success(self) -> None:
        """Test successful version extraction from pyproject.toml."""
        mock_content = b"""
[project]
name = "test-app"
version = "1.2.3"
"""
        with (
            patch("builtins.open", mock_open(read_data=mock_content)),
            patch("pathlib.Path.open", mock_open(read_data=mock_content)),
        ):
            version = _get_version_from_pyproject()
            assert version == "1.2.3"

    def test_get_version_file_not_found(self) -> None:
        """Test version extraction when pyproject.toml doesn't exist."""
        with patch("pathlib.Path.open", side_effect=FileNotFoundError):
            version = _get_version_from_pyproject()
            assert version == "unknown"

    def test_get_version_key_error(self) -> None:
        """Test version extraction with missing version key."""
        mock_content = b"""
[project]
name = "test-app"
"""
        with patch("pathlib.Path.open", mock_open(read_data=mock_content)):
            version = _get_version_from_pyproject()
            assert version == "unknown"

    def test_get_version_invalid_toml(self) -> None:
        """Test version extraction with invalid TOML."""
        mock_content = b"invalid toml content"
        with patch("pathlib.Path.open", mock_open(read_data=mock_content)):
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
