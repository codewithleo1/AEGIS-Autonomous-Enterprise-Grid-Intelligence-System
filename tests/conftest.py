import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

API_KEY = "aegis-secret-123"


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers():
    return {"X-API-Key": API_KEY}
