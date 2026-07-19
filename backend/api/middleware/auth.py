from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.config import settings
from backend.services.auth_service import decode_token
from jose import JWTError

PUBLIC_ROUTES = {"/health", "/docs", "/openapi.json", "/redoc", "/auth/login"}

# Routes that require agent-level API key (internal/service use)
API_KEY_ROUTES = {"/ask", "/session"}


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow CORS preflight through
        if request.method == "OPTIONS":
            return await call_next(request)

        # Allow public routes through without any auth
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        # Check for JWT token first
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                decode_token(token)
                return await call_next(request)
            except JWTError:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Invalid or expired token."},
                )

        # Fall back to API key for backwards compatibility
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"error": "Missing API key. Include X-API-Key header."},
            )

        if api_key != settings.aegis_api_key:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid API key."},
            )

        return await call_next(request)