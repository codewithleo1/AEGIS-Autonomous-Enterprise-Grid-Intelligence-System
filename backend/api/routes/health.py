from fastapi import APIRouter
from backend.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Simple health check — used by Docker and Fly.io to verify the app is running."""
    return {
        "status": "ok",
        "app": "AEGIS",
        "version": settings.app_version,
        "env": settings.app_env,
    }