import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

API_KEY = "aegis-secret-123"


@pytest.fixture
def client():
    # Patch create_tables so TestClient doesn't connect to real DB
    with patch("backend.db.postgres.create_tables", new_callable=AsyncMock):
        from backend.main import app
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c


@pytest.fixture
def auth_headers():
    return {"X-API-Key": API_KEY}
