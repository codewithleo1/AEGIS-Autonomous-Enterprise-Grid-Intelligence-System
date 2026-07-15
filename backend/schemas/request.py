from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    session_id: str = Field(..., description="Unique session ID for conversation memory")
    message: str = Field(..., description="The user's message to AEGIS")
    employee_id: str = Field(..., description="TechCorp Employee ID e.g. EMP001")