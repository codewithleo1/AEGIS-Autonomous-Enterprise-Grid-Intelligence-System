from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.config import settings

# Routes that don't require an API key
PUBLIC_ROUTES = {"/health", "/docs", "/openapi.json", "/redoc"}


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Checks every request for a valid X-API-Key header.
    Rejects with 401 if the key is missing or incorrect.
    Public routes (health, docs) are exempt.
    """

    async def dispatch(self, request: Request, call_next):
        # Allow public routes through without a key
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        # Check for the API key header
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

        # Key is valid — pass request through to the route
        return await call_next(request)