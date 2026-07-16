from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.config import settings

PUBLIC_ROUTES = {"/health", "/docs", "/openapi.json", "/redoc"}


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow CORS preflight through — browser sends OPTIONS before every POST
        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

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