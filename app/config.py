"""Application configuration."""

import logging
import tomllib
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


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


class Settings(BaseSettings):
    """Application settings with validation and environment variable support."""

    # Application settings
    app_name: str = Field(default="Portia FastAPI Example", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")

    # Server settings
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # CORS settings
    allowed_domains: list[str] = Field(
        default=["*"], description="List of allowed domains for CORS"
    )

    # Portia SDK settings
    portia_api_key: str | None = Field(default=None, description="Portia API key")

    # LLM settings
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    anthropic_api_key: str | None = Field(default=None, description="Anthropic API key")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")

    # Application version
    application_version: str = Field(
        default_factory=_get_version_from_pyproject, description="Application version"
    )


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
