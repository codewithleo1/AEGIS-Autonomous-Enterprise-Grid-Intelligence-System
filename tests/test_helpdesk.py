from unittest.mock import patch, AsyncMock
from backend.schemas.response import ToolCall


def test_ask_returns_reply(client, auth_headers):
    with patch("backend.api.routes.helpdesk.run_agent", new_callable=AsyncMock, return_value=("Hello from AEGIS", [])):
        response = client.post("/ask",
            json={"session_id": "test-s1", "message": "hi", "employee_id": "EMP001"},
            headers=auth_headers,
        )
    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "Hello from AEGIS"
    assert data["session_id"] == "test-s1"
    assert data["tools_used"] == []


def test_ask_returns_tools_used(client, auth_headers):
    mock_tool = ToolCall(
        tool_name="get_ticket_status",
        args={"ticket_id": "TKT-001"},
        result={"status": "Open"},
    )
    with patch("backend.api.routes.helpdesk.run_agent", new_callable=AsyncMock, return_value=("Ticket is Open", [mock_tool])):
        response = client.post("/ask",
            json={"session_id": "test-s2", "message": "status of TKT-001", "employee_id": "EMP001"},
            headers=auth_headers,
        )
    assert response.status_code == 200
    data = response.json()
    assert len(data["tools_used"]) == 1
    assert data["tools_used"][0]["tool_name"] == "get_ticket_status"


def test_ask_maintains_session_history(client, auth_headers):
    with patch("backend.api.routes.helpdesk.run_agent", new_callable=AsyncMock, return_value=("Reply 1", [])) as mock:
        client.post("/ask",
            json={"session_id": "test-s3", "message": "first message", "employee_id": "EMP001"},
            headers=auth_headers,
        )
        client.post("/ask",
            json={"session_id": "test-s3", "message": "second message", "employee_id": "EMP001"},
            headers=auth_headers,
        )
        second_call_history = mock.call_args[0][0]
        assert any(m["content"] == "first message" for m in second_call_history)


def test_delete_session(client, auth_headers):
    with patch("backend.api.routes.helpdesk.run_agent", new_callable=AsyncMock, return_value=("hi", [])):
        client.post("/ask",
            json={"session_id": "test-s4", "message": "hello", "employee_id": "EMP001"},
            headers=auth_headers,
        )
    response = client.delete("/session/test-s4", headers=auth_headers)
    assert response.status_code == 200


def test_delete_nonexistent_session_returns_404(client, auth_headers):
    response = client.delete("/session/nonexistent-session", headers=auth_headers)
    assert response.status_code == 404
