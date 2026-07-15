from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    tool_name: str = Field(..., description="Name of the tool that was called")
    args: dict = Field(..., description="Arguments passed to the tool")
    result: dict = Field(..., description="Result returned by the tool")


class AskResponse(BaseModel):
    session_id: str = Field(..., description="Echo back the session ID")
    reply: str = Field(..., description="AEGIS's final human-readable reply")
    tools_used: list[ToolCall] = Field(
        default_factory=list,
        description="All tool calls made during this request"
    )