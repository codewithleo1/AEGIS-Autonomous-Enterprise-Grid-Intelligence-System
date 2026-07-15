files = {}

files["tests/conftest.py"] = """import pytest
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
"""

files["tests/test_health.py"] = """def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_correct_fields(client):
    data = client.get("/health").json()
    assert data["status"] == "ok"
    assert data["app"] == "AEGIS"
    assert "version" in data
    assert "env" in data
"""

files["tests/test_auth.py"] = """def test_missing_api_key_returns_401(client):
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
"""

files["tests/test_helpdesk.py"] = """from unittest.mock import patch, AsyncMock
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
"""

files["tests/test_employee_service.py"] = """import asyncio
from unittest.mock import MagicMock, patch, AsyncMock


def make_mock_session(return_value):
    mock_session = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = return_value
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    mock_session.execute = AsyncMock(return_value=mock_result)
    return mock_session


def make_mock_emp():
    emp = MagicMock()
    emp.employee_id = "EMP001"
    emp.name = "Raj Sharma"
    emp.department = "Engineering"
    emp.email = "raj.sharma@techcorp.com"
    emp.manager = "EMP010"
    emp.location = "Mumbai"
    return emp


def test_get_existing_employee():
    mock_session = make_mock_session(make_mock_emp())
    with patch("backend.services.employee_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.employee_service import get_employee_info_async
        result = asyncio.run(get_employee_info_async("EMP001"))
    assert result["name"] == "Raj Sharma"
    assert result["employee_id"] == "EMP001"


def test_get_nonexistent_employee_returns_error():
    mock_session = make_mock_session(None)
    with patch("backend.services.employee_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.employee_service import get_employee_info_async
        result = asyncio.run(get_employee_info_async("EMP999"))
    assert "error" in result


def test_get_employee_case_insensitive():
    mock_session = make_mock_session(make_mock_emp())
    with patch("backend.services.employee_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.employee_service import get_employee_info_async
        result = asyncio.run(get_employee_info_async("emp001"))
    assert result["name"] == "Raj Sharma"
"""

files["tests/test_ticket_service.py"] = """import asyncio
from unittest.mock import MagicMock, patch, AsyncMock


def make_mock_session_scalar(return_value):
    mock_session = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = return_value
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    return mock_session


def make_mock_session_scalars(return_list):
    mock_session = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = return_list
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    mock_session.execute = AsyncMock(return_value=mock_result)
    return mock_session


def make_mock_ticket():
    t = MagicMock()
    t.ticket_id = "TKT-001"
    t.title = "WiFi not connecting"
    t.employee_id = "EMP001"
    t.priority = "HIGH"
    t.status = "Open"
    t.category = "Network"
    t.assigned_agent = "AGT-003"
    t.assigned_agent_name = "Tarun Bose"
    t.created = "2025-07-01"
    t.updated = "2025-07-01"
    return t


def test_get_existing_ticket():
    mock_session = make_mock_session_scalar(make_mock_ticket())
    with patch("backend.services.ticket_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.ticket_service import get_ticket_status_async
        result = asyncio.run(get_ticket_status_async("TKT-001"))
    assert result["ticket_id"] == "TKT-001"
    assert result["status"] == "Open"


def test_get_nonexistent_ticket_returns_error():
    mock_session = make_mock_session_scalar(None)
    with patch("backend.services.ticket_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.ticket_service import get_ticket_status_async
        result = asyncio.run(get_ticket_status_async("TKT-999"))
    assert "error" in result


def test_list_tickets_returns_results():
    mock_session = make_mock_session_scalars([make_mock_ticket()])
    with patch("backend.services.ticket_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.ticket_service import list_tickets_async
        result = asyncio.run(list_tickets_async())
    assert result["total"] == 1
    assert result["tickets"][0]["ticket_id"] == "TKT-001"


def test_update_ticket_status():
    mock_ticket = make_mock_ticket()
    mock_session = make_mock_session_scalar(mock_ticket)
    with patch("backend.services.ticket_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.ticket_service import update_ticket_async
        result = asyncio.run(update_ticket_async("TKT-001", "Resolved", "Fixed"))
    assert result["new_status"] == "Resolved"
    assert result["note"] == "Fixed"


def test_update_nonexistent_ticket_returns_error():
    mock_session = make_mock_session_scalar(None)
    with patch("backend.services.ticket_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.ticket_service import update_ticket_async
        result = asyncio.run(update_ticket_async("TKT-999", "Resolved"))
    assert "error" in result


def test_create_ticket_assigns_correct_agent():
    mock_session = MagicMock()
    mock_count_result = MagicMock()
    mock_count_result.scalar.return_value = 20
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    mock_session.execute = AsyncMock(return_value=mock_count_result)
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    with patch("backend.services.ticket_service.AsyncSessionLocal", return_value=mock_session):
        from backend.services.ticket_service import create_ticket_async
        result = asyncio.run(create_ticket_async("EMP001", "Test", "HIGH", "Network", "desc"))
    assert result["assigned_agent_name"] == "Tarun Bose"
    assert result["status"] == "Open"
    assert result["ticket_id"] == "TKT-021"
"""

files["tests/test_report_service.py"] = """import asyncio
from unittest.mock import MagicMock, patch, AsyncMock


def make_mock_tickets():
    tickets = []
    data = [
        ("Open", "HIGH", "Network"),
        ("Open", "CRITICAL", "Hardware"),
        ("Resolved", "MEDIUM", "Software"),
        ("In Progress", "LOW", "Authentication"),
    ]
    for i, (s, p, c) in enumerate(data):
        t = MagicMock()
        t.status = s
        t.priority = p
        t.category = c
        t.employee_id = "EMP001"
        t.created = "2025-07-01"
        tickets.append(t)
    return tickets


def make_mock_session(tickets):
    mock_session = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = tickets
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    mock_session.execute = AsyncMock(return_value=mock_result)
    return mock_session


def test_report_returns_required_fields():
    with patch("backend.services.report_service.AsyncSessionLocal", return_value=make_mock_session(make_mock_tickets())):
        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async())
    assert "total_tickets" in result
    assert "breakdown" in result
    assert "avg_resolution_time" in result


def test_report_filter_by_status():
    with patch("backend.services.report_service.AsyncSessionLocal", return_value=make_mock_session(make_mock_tickets())):
        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async(filter_by="status"))
    assert "Open" in result["breakdown"]


def test_report_filter_by_priority():
    with patch("backend.services.report_service.AsyncSessionLocal", return_value=make_mock_session(make_mock_tickets())):
        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async(filter_by="priority"))
    assert "HIGH" in result["breakdown"]


def test_report_filter_by_category():
    with patch("backend.services.report_service.AsyncSessionLocal", return_value=make_mock_session(make_mock_tickets())):
        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async(filter_by="category"))
    assert "Network" in result["breakdown"]


def test_report_total_matches_mock():
    with patch("backend.services.report_service.AsyncSessionLocal", return_value=make_mock_session(make_mock_tickets())):
        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async())
    assert result["total_tickets"] == 4
"""

files["tests/test_tool_executor.py"] = """import asyncio
from unittest.mock import AsyncMock, patch


def test_execute_known_tool():
    with patch("backend.agent.tool_executor.get_ticket_status_async", new_callable=AsyncMock, return_value={"ticket_id": "TKT-001", "status": "Open"}):
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("get_ticket_status", {"ticket_id": "TKT-001"}))
    assert result["ticket_id"] == "TKT-001"


def test_execute_unknown_tool_returns_error():
    from backend.agent.tool_executor import execute_tool
    result = asyncio.run(execute_tool("nonexistent_tool", {}))
    assert "error" in result
    assert "Unknown tool" in result["error"]


def test_execute_get_employee_info():
    with patch("backend.agent.tool_executor.get_employee_info_async", new_callable=AsyncMock, return_value={"name": "Raj Sharma", "employee_id": "EMP001"}):
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("get_employee_info", {"employee_id": "EMP001"}))
    assert result["name"] == "Raj Sharma"


def test_execute_list_tickets():
    with patch("backend.agent.tool_executor.list_tickets_async", new_callable=AsyncMock, return_value={"total": 5, "tickets": []}):
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("list_tickets", {"status": "Open"}))
    assert result["total"] == 5


def test_execute_tool_handles_exception_gracefully():
    with patch("backend.agent.tool_executor.get_ticket_status_async", new_callable=AsyncMock, side_effect=Exception("DB error")):
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("get_ticket_status", {"ticket_id": "TKT-001"}))
    assert "error" in result


def test_execute_create_ticket():
    with patch("backend.agent.tool_executor.create_ticket_async", new_callable=AsyncMock, return_value={"ticket_id": "TKT-021", "status": "Open"}):
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("create_ticket", {
            "employee_id": "EMP001", "title": "Test",
            "priority": "LOW", "category": "Other", "description": "Test",
        }))
    assert result["ticket_id"] == "TKT-021"
"""

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written: {path}")

print("\nAll test files written successfully.")