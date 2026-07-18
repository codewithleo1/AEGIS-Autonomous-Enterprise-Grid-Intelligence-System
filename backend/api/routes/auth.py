from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.services.auth_service import login

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    id: str
    name: str


@router.post("/login", response_model=LoginResponse)
async def auth_login(body: LoginRequest):
    """
    Authenticate an employee or agent.
    Returns a JWT token with role information.
    """
    result = await login(email=body.email, password=body.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return result