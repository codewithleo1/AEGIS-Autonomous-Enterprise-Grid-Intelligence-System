def test_missing_api_key_returns_401(client):
    response = client.post("/ask", json={
        "session_id": "s1",
        "message": "hello",
        "employee_id": "EMP001",
    })
    assert response.status_code == 401
    assert "Missing API key" in response.json()["error"]


def test_wrong_api_key_returns_401(client):
    response = client.post("/ask",
        json={"session_id": "s1", "message": "hello", "employee_id": "EMP001"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["error"]


def test_valid_api_key_does_not_return_401(client, auth_headers):
    from unittest.mock import patch, AsyncMock
    with patch("backend.api.routes.helpdesk.run_agent", new_callable=AsyncMock, return_value=("hello", [])):
        response = client.post("/ask",
            json={"session_id": "s1", "message": "hello", "employee_id": "EMP001"},
            headers=auth_headers,
        )
    assert response.status_code != 401
