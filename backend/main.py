from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.api.middleware.auth import APIKeyMiddleware
from backend.api.middleware.rate_limit import limiter
from backend.api.routes import health, helpdesk, tickets
from backend.config import settings
from backend.db.postgres import create_tables
from backend.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────
    logger.info("AEGIS v%s starting in %s mode", settings.app_version, settings.app_env)
    await create_tables()
    logger.info("Database ready")
    yield
    # ── Shutdown ─────────────────────────────────────────────────
    logger.info("AEGIS shutting down")


app = FastAPI(
    title="AEGIS",
    description="Autonomous Enterprise Grid Intelligence System — TechCorp IT Helpdesk AI",
    version=settings.app_version,
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(APIKeyMiddleware)

# ── Routes ────────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(helpdesk.router)
app.include_router(tickets.router)