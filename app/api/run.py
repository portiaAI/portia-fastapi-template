"""API endpoints for the /run functionality."""

import logging

from fastapi import APIRouter, HTTPException, status

from app.exceptions import InvalidToolsError
from app.schemas.run import RunRequest, RunResponse
from app.services.portia_service import PortiaService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/run",
    status_code=status.HTTP_200_OK,
    summary="Execute a query using the Portia SDK",
    description=(
        "Accepts a query and optional tools list, then executes the query using the Portia SDK"
    ),
)
async def run_query(
    request: RunRequest,
) -> RunResponse:
    """Execute a query using the Portia SDK.

    - **query**: The query to execute
    - **tools**: List of tool IDs to use
    Returns the result of the query execution.
    """
    try:
        logger.info(f"Received run request: query='{request.query}', tools={request.tools}")

        # Execute the query using the Portia service
        result = await PortiaService.get_instance().run_query(
            query=request.query, tools=request.tools
        )
        return RunResponse(
            success=result["success"],
            result=result.get("result"),
            error=result.get("error"),
            execution_time=result.get("execution_time"),
        )

    except InvalidToolsError as e:
        logger.warning(f"Invalid tools requested: {e.invalid_tools}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid tools requested",
                "message": str(e),
                "invalid_tools": e.invalid_tools,
                "available_tools": e.available_tools,
            },
        ) from e
    except Exception as e:
        logger.exception("Unexpected error in run_query")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e!s}",
        ) from e


@router.get(
    "/tools",
    status_code=status.HTTP_200_OK,
    summary="Get available tools",
    description="Get a list of available tools from the Portia SDK",
)
async def get_available_tools() -> list[str]:
    """Get available tools.

    Returns a list of available tool names.
    """
    portia = PortiaService.get_instance()

    try:
        return portia.available_tool_ids()
    except Exception as e:
        logger.exception("Failed to get available tools")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get available tools: {e!s}",
        ) from e
