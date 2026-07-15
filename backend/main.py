from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.api.middleware.auth import APIKeyMiddleware
from backend.api.middleware.rate_limit import limiter
from backend.api.routes import health, helpdesk, tickets
from backend.config import settings
from backend.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="AEGIS",
    description="Autonomous Enterprise Grid Intelligence System",
    version=settings.app_version,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(APIKeyMiddleware)

app.include_router(health.router)
app.include_router(helpdesk.router)
app.include_router(tickets.router)

logger.info("AEGIS v%s started in %s mode", settings.app_version, settings.app_env)
