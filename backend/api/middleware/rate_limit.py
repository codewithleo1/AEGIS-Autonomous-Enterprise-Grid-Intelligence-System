from slowapi import Limiter
from slowapi.util import get_remote_address


def get_api_key(request) -> str:
    """
    Use the API key as the rate limit identifier.
    Falls back to IP address if no key present (e.g. /health endpoint).
    """
    return request.headers.get("X-API-Key") or get_remote_address(request)


# Global limiter instance — imported into main.py and routes
limiter = Limiter(key_func=get_api_key)