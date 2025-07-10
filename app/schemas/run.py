"""Pydantic schemas for the /run endpoint."""

from typing import Any

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    """Request model for the /run endpoint."""

    query: str = Field(
        ...,
        description="The query to execute using the Portia SDK",
        min_length=1,
    )
    tools: list[str] = Field(
        ...,
        description="List of tool IDs to use for the execution",
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "What is 2+2?",
                    "tools": ["calculator_tool"],
                }
            ]
        }
    }


class RunResponse(BaseModel):
    """Response model for the /run endpoint."""

    success: bool = Field(..., description="Whether the execution was successful")
    result: Any | None = Field(default=None, description="The result of the execution")
    error: str | None = Field(default=None, description="Error message if execution failed")
    execution_time: float | None = Field(default=None, description="Execution time in seconds")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "result": {
                        "value": "4.0",
                        "summary": (
                            "The query asked for the result of 2+2, and the expression "
                            "was evaluated to give the output 4.0."
                        ),
                    },
                    "error": None,
                    "execution_time": 2.5,
                }
            ]
        }
    }
