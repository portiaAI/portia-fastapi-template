"""Portia SDK service integration."""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import ClassVar

from portia import DefaultToolRegistry, Portia, Tool

from app.config import settings
from app.exceptions import InvalidToolsError

logger = logging.getLogger(__name__)


class PortiaService:
    """Singleton service for interacting with the Portia SDK.

    This class ensures only one instance of the Portia service exists
    throughout the application lifecycle.
    """

    _instance: ClassVar["PortiaService | None"] = None

    def __new__(cls) -> "PortiaService":
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "PortiaService":
        """Get the singleton instance of PortiaService."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        """Initialize the Portia service."""
        if not hasattr(self, "_initialized"):
            self._config = settings.get_portia_config()
            self._initialized = True
            self._tools: set[str] = set()
            self._portia_instance: Portia | None = None
            self._executor = ThreadPoolExecutor(max_workers=settings.max_workers)

    def _get_portia_instance(self, tools: set[str]) -> Portia:
        """Get the Portia SDK instance for the given tools.

        Args:
            tools: Set of tool IDs to use

        Raises:
            InvalidToolsError: If requested tools are not available

        """
        if tools == self._tools and self._portia_instance is not None:
            return self._portia_instance

        available_tools_map = self._get_available_tools_map()

        if tools.issubset(set(available_tools_map.keys())):
            self._portia_instance = Portia(
                config=self._config,
                tools=[available_tools_map[tool] for tool in tools],
                execution_hooks=None,  # No CLI hooks for API usage
            )
            self._tools = tools
            logger.info(f"Portia SDK initialized successfully with tools: {tools}")

            return self._portia_instance

        raise InvalidToolsError(list(tools), list(available_tools_map.keys()))

    async def run_query(self, query: str, tools: list[str]) -> dict:
        """Run the given query using the Portia SDK and specified tools.

        Args:
            query: The query to execute
            tools: List of tool IDs to use

        Returns:
            The result of the query execution

        Raises:
            InvalidToolsError: If requested tools are not available

        """
        portia_instance = self._get_portia_instance(set(tools))

        start_time = time.time()

        try:
            # Run the Portia execution in a thread pool to avoid blocking the event loop
            loop = asyncio.get_running_loop()
            plan_run = await loop.run_in_executor(self._executor, portia_instance.run, query, tools)

            result = plan_run.outputs.final_output

            execution_time = round(time.time() - start_time, 2)

            logger.info(f"Query executed successfully in {execution_time}s")

        except Exception as e:
            execution_time = time.time() - start_time
            logger.exception(f"Query execution failed after {execution_time}s")

            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
            }
        else:
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
            }

    def available_tool_ids(self) -> list[str]:
        """Get list of available tool IDs."""
        return list(self._get_available_tools_map().keys())

    def _get_available_tools_map(self) -> dict[str, Tool]:
        """Get a map of tool IDs to tool objects for all the available tools."""
        available_tools = DefaultToolRegistry(config=self._config).get_tools()
        return {tool.id: tool for tool in available_tools}
