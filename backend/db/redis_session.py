import json

from upstash_redis import Redis

from backend.config import settings
from backend.logger import setup_logger

logger = setup_logger(__name__)

# Session key prefix — all AEGIS sessions stored as "session:{session_id}"
SESSION_PREFIX = "session:"

# TTL — sessions expire after 24 hours of inactivity (in seconds)
SESSION_TTL = 60 * 60 * 24


def _get_client() -> Redis:
    """Create a new Upstash Redis client using REST URL + token from config."""
    return Redis(
        url=settings.upstash_redis_rest_url,
        token=settings.upstash_redis_rest_token,
    )


def load_session(session_id: str) -> list[dict]:
    """
    Load conversation history for a session from Redis.
    Returns empty list if session does not exist yet.
    """
    try:
        client = _get_client()
        key = f"{SESSION_PREFIX}{session_id}"
        data = client.get(key)

        if data is None:
            logger.debug("No existing session found for: %s", session_id)
            return []

        history = json.loads(data)
        logger.debug("Loaded session %s — %d messages", session_id, len(history))
        return history

    except Exception as e:
        logger.error("Failed to load session %s: %s", session_id, str(e))
        return []


def save_session(session_id: str, history: list[dict]) -> None:
    """
    Save conversation history for a session to Redis.
    Resets the TTL on every save so active sessions don't expire.
    """
    try:
        client = _get_client()
        key = f"{SESSION_PREFIX}{session_id}"
        client.set(key, json.dumps(history), ex=SESSION_TTL)
        logger.debug("Saved session %s — %d messages", session_id, len(history))

    except Exception as e:
        logger.error("Failed to save session %s: %s", session_id, str(e))


def delete_session(session_id: str) -> bool:
    """
    Delete a session from Redis.
    Returns True if deleted, False if session did not exist.
    """
    try:
        client = _get_client()
        key = f"{SESSION_PREFIX}{session_id}"
        result = client.delete(key)
        logger.debug("Deleted session %s", session_id)
        return result > 0

    except Exception as e:
        logger.error("Failed to delete session %s: %s", session_id, str(e))
        return False
