from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from backend.services.auth_service import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    """
    FastAPI dependency — extracts and validates JWT from Authorization header.
    Returns the decoded token payload: { sub, role, name }
    Raises 401 if token is missing or invalid.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Include Authorization: Bearer <token>",
        )

    try:
        payload = decode_token(credentials.credentials)
        return {
            "id": payload["sub"],
            "role": payload["role"],
            "name": payload["name"],
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )


def require_agent(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency that only allows agents through."""
    if current_user["role"] != "agent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent access required.",
        )
    return current_user


def require_employee(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency that only allows employees through."""
    if current_user["role"] != "employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee access required.",
        )
    return current_user