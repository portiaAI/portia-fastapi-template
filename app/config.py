"""Application configuration."""

import logging
import tomllib
from pathlib import Path
from typing import Any

from portia.config import Config as PortiaConfig
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _get_version_from_pyproject() -> str:
    """Extract version from pyproject.toml file."""
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError) as e:
        logging.getLogger(__name__).warning(f"Could not read version from pyproject.toml: {e}")
        return "unknown"


class PortiaConfigSettings(BaseSettings):
    """Portia configuration settings."""

    # API Keys
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    anthropic_api_key: str | None = Field(default=None, description="Anthropic API key")
    mistralai_api_key: str | None = Field(default=None, description="MistralAI API key")
    google_api_key: str | None = Field(default=None, description="Google Generative AI API key")
    azure_openai_api_key: str | None = Field(default=None, description="Azure OpenAI API key")
    portia_api_key: str | None = Field(default=None, description="Portia API key")

    # API Endpoints
    portia_api_endpoint: str | None = Field(default=None, description="Portia API endpoint")
    portia_dashboard_url: str | None = Field(default=None, description="Portia Dashboard URL")
    azure_openai_endpoint: str | None = Field(default=None, description="Azure OpenAI endpoint")
    ollama_base_url: str | None = Field(default=None, description="Ollama base URL")

    # LLM Configuration
    llm_provider: str | None = Field(default=None, description="LLM provider")
    llm_redis_cache_url: str | None = Field(
        default=None, description="Redis cache URL for LLM responses"
    )

    # Model Configuration
    default_model: str | None = Field(default=None, description="Default generative model")
    planning_model: str | None = Field(default=None, description="Planning agent model")
    execution_model: str | None = Field(default=None, description="Execution agent model")
    introspection_model: str | None = Field(default=None, description="Introspection agent model")
    summarizer_model: str | None = Field(default=None, description="Summarizer agent model")

    # Storage Configuration
    storage_class: str | None = Field(
        default=None, description="Storage class (MEMORY, DISK, CLOUD)"
    )
    storage_dir: str | None = Field(default=None, description="Storage directory for DISK storage")

    # Logging Configuration
    default_log_level: str | None = Field(default=None, description="Default log level")
    default_log_sink: str | None = Field(default=None, description="Default log sink")
    json_log_serialize: bool | None = Field(default=None, description="JSON serialize logs")

    # Agent Configuration
    planning_agent_type: str | None = Field(default=None, description="Planning agent type")
    execution_agent_type: str | None = Field(default=None, description="Execution agent type")
    large_output_threshold_tokens: int | None = Field(
        default=None, description="Large output threshold in tokens"
    )

    # Feature Flags and Other Settings
    feature_flags: dict[str, bool] | None = Field(default=None, description="Feature flags")
    argument_clarifications_enabled: bool | None = Field(
        default=None, description="Enable argument clarifications"
    )

    model_config = SettingsConfigDict(env_prefix="PORTIA_CONFIG_")

    def to_portia_config(self) -> PortiaConfig:
        """Convert settings to Portia Config."""
        config_data = self.model_dump(exclude_none=True)

        return PortiaConfig.from_default(**config_data)


class Settings(BaseSettings):
    """Application settings with validation and environment variable support."""

    # Application settings
    app_name: str = Field(default="Portia FastAPI Example", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")

    # Server settings
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port")
    max_workers: int = Field(
        default=4, description="Maximum number of worker threads for Portia execution"
    )

    # CORS settings
    allowed_domains: list[str] = Field(
        default=["*"], description="List of allowed domains for CORS"
    )

    # Portia configuration
    portia_config: PortiaConfigSettings = Field(
        default_factory=PortiaConfigSettings, description="Portia configuration"
    )

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")

    # Application version
    application_version: str = Field(
        default_factory=_get_version_from_pyproject, description="Application version"
    )

    model_config = SettingsConfigDict(env_nested_delimiter="__")

    def get_portia_config(self) -> PortiaConfig:
        """Get the Portia configuration."""
        return self.portia_config.to_portia_config()


settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def get_app_config() -> dict[str, Any]:
    """Get application configuration."""
    return {}
