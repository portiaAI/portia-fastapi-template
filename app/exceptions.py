"""Custom exceptions for the application."""


class InvalidToolsError(Exception):
    """Exception raised when requested tools are not available.

    This exception is raised when a user requests tools that are not
    in the available tools list from the Portia SDK.
    """

    def __init__(self, invalid_tools: list[str], available_tools: list[str]) -> None:
        """Initialize the exception.

        Args:
            invalid_tools: List of tools that were requested but not available
            available_tools: List of all available tools

        """
        self.invalid_tools = invalid_tools
        self.available_tools = available_tools
        super().__init__(
            f"The following tools are not available: {', '.join(invalid_tools)}. "
            f"Available tools: {', '.join(available_tools)}"
        )
