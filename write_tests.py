import os

os.makedirs("tests", exist_ok=True)

files = {}

files["tests/__init__.py"] = ""

files["tests/conftest.py"] = """import pytest
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
"""

files["tests/test_health.py"] = """def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_correct_fields(client):
    data = response = client.get("/health").json()
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
    # We mock run_agent so we don't call real Groq
    from unittest.mock import patch
    with patch("backend.api.routes.helpdesk.run_agent", return_value=("hello", [])):
        response = client.post("/ask",
            json={"session_id": "s1", "message": "hello", "employee_id": "EMP001"},
            headers=auth_headers,
        )
    assert response.status_code != 401
"""

files["tests/test_employee_service.py"] = """from backend.services.employee_service import get_employee_info


def test_get_existing_employee():
    result = get_employee_info("EMP001")
    assert result["name"] == "Raj Sharma"
    assert result["department"] == "Engineering"
    assert result["email"] == "raj.sharma@techcorp.com"
    assert result["location"] == "Mumbai"


def test_get_employee_case_insensitive():
    result = get_employee_info("emp001")
    assert result["name"] == "Raj Sharma"


def test_get_nonexistent_employee_returns_error():
    result = get_employee_info("EMP999")
    assert "error" in result


def test_all_employees_have_required_fields():
    from backend.services.employee_service import EMPLOYEES
    required = {"employee_id", "name", "department", "email", "location"}
    for emp_id, emp in EMPLOYEES.items():
        for field in required:
            assert field in emp, f"{emp_id} missing field: {field}"
"""

files["tests/test_ticket_service.py"] = """import pytest
from backend.services.ticket_service import (
    create_ticket,
    get_ticket_status,
    list_tickets,
    update_ticket,
    TICKETS,
)


def test_get_existing_ticket():
    result = get_ticket_status("TKT-001")
    assert result["ticket_id"] == "TKT-001"
    assert result["status"] == "Open"
    assert result["priority"] == "HIGH"


def test_get_ticket_case_insensitive():
    result = get_ticket_status("tkt-001")
    assert result["ticket_id"] == "TKT-001"


def test_get_nonexistent_ticket_returns_error():
    result = get_ticket_status("TKT-999")
    assert "error" in result


def test_create_ticket_returns_correct_fields():
    result = create_ticket(
        employee_id="EMP001",
        title="Test issue",
        priority="HIGH",
        category="Network",
        description="Test description",
    )
    assert "ticket_id" in result
    assert result["status"] == "Open"
    assert result["priority"] == "HIGH"
    assert result["assigned_agent_name"] == "Tarun Bose"
    assert result["employee_id"] == "EMP001"


def test_create_ticket_auto_assigns_correct_agent():
    agents = {
        "Hardware": "Kiran Pillai",
        "Software": "Nisha Gupta",
        "Network": "Tarun Bose",
        "Authentication": "Salma Shaikh",
        "Other": "Dev Malhotra",
    }
    for category, expected_agent in agents.items():
        result = create_ticket(
            employee_id="EMP001",
            title=f"Test {category}",
            priority="LOW",
            category=category,
            description="Test",
        )
        assert result["assigned_agent_name"] == expected_agent


def test_create_ticket_increments_id():
    t1 = create_ticket("EMP001", "Issue A", "LOW", "Other", "desc")
    t2 = create_ticket("EMP001", "Issue B", "LOW", "Other", "desc")
    num1 = int(t1["ticket_id"].split("-")[1])
    num2 = int(t2["ticket_id"].split("-")[1])
    assert num2 == num1 + 1


def test_list_tickets_no_filter_returns_all():
    result = list_tickets()
    assert result["total"] >= 20
    assert len(result["tickets"]) >= 20


def test_list_tickets_filter_by_status():
    result = list_tickets(status="Open")
    for ticket in result["tickets"]:
        assert ticket["status"] == "Open"


def test_list_tickets_filter_by_priority():
    result = list_tickets(priority="CRITICAL")
    for ticket in result["tickets"]:
        assert ticket["priority"] == "CRITICAL"


def test_list_tickets_filter_by_employee():
    result = list_tickets(employee_id="EMP001")
    for ticket in result["tickets"]:
        assert ticket["employee_id"] == "EMP001"


def test_list_tickets_filter_by_category():
    result = list_tickets(category="Network")
    for ticket in result["tickets"]:
        assert ticket["category"] == "Network"


def test_update_ticket_status():
    result = update_ticket("TKT-003", "Open")
    assert result["old_status"] == "Resolved"
    assert result["new_status"] == "Open"
    # Reset it back
    update_ticket("TKT-003", "Resolved")


def test_update_ticket_with_note():
    result = update_ticket("TKT-005", "Resolved", note="Driver reinstalled")
    assert result["new_status"] == "Resolved"
    assert result["note"] == "Driver reinstalled"
    # Reset
    update_ticket("TKT-005", "Open")


def test_update_nonexistent_ticket_returns_error():
    result = update_ticket("TKT-999", "Resolved")
    assert "error" in result
"""

files["tests/test_report_service.py"] = """from backend.services.report_service import generate_report


def test_report_returns_required_fields():
    result = generate_report()
    assert "total_tickets" in result
    assert "breakdown" in result
    assert "avg_resolution_time" in result


def test_report_total_matches_mock_data():
    result = generate_report()
    assert result["total_tickets"] >= 20


def test_report_filter_by_status():
    result = generate_report(filter_by="status")
    breakdown = result["breakdown"]
    assert "Open" in breakdown
    assert "Resolved" in breakdown
    assert "In Progress" in breakdown


def test_report_filter_by_priority():
    result = generate_report(filter_by="priority")
    breakdown = result["breakdown"]
    assert "HIGH" in breakdown
    assert "CRITICAL" in breakdown


def test_report_filter_by_category():
    result = generate_report(filter_by="category")
    breakdown = result["breakdown"]
    assert "Hardware" in breakdown
    assert "Network" in breakdown


def test_report_filter_by_department():
    result = generate_report(filter_by="department")
    breakdown = result["breakdown"]
    assert "Engineering" in breakdown


def test_report_date_filter():
    result = generate_report(date_from="2025-07-10", date_to="2025-07-14")
    assert result["total_tickets"] < 20


def test_report_default_breakdown_has_all_keys():
    result = generate_report()
    breakdown = result["breakdown"]
    assert "by_status" in breakdown
    assert "by_priority" in breakdown
    assert "by_category" in breakdown
"""

files["tests/test_tool_executor.py"] = """from unittest.mock import patch
from backend.agent.tool_executor import execute_tool


def test_execute_known_tool():
    result = execute_tool("get_ticket_status", {"ticket_id": "TKT-001"})
    assert result["ticket_id"] == "TKT-001"


def test_execute_unknown_tool_returns_error():
    result = execute_tool("nonexistent_tool", {})
    assert "error" in result
    assert "Unknown tool" in result["error"]


def test_execute_get_employee_info():
    result = execute_tool("get_employee_info", {"employee_id": "EMP001"})
    assert result["name"] == "Raj Sharma"


def test_execute_list_tickets():
    result = execute_tool("list_tickets", {"status": "Open"})
    assert "tickets" in result
    assert result["total"] > 0


def test_execute_tool_handles_exception_gracefully():
    # Pass wrong args to trigger an exception
    result = execute_tool("get_ticket_status", {})
    assert "error" in result


def test_execute_create_ticket():
    result = execute_tool("create_ticket", {
        "employee_id": "EMP001",
        "title": "Test via executor",
        "priority": "LOW",
        "category": "Other",
        "description": "Testing tool executor",
    })
    assert "ticket_id" in result
    assert result["status"] == "Open"
"""

files["tests/test_helpdesk.py"] = """from unittest.mock import patch
from backend.schemas.response import ToolCall


def test_ask_returns_reply(client, auth_headers):
    with patch("backend.api.routes.helpdesk.run_agent", return_value=("Hello from AEGIS", [])):
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
    with patch("backend.api.routes.helpdesk.run_agent", return_value=("Ticket is Open", [mock_tool])):
        response = client.post("/ask",
            json={"session_id": "test-s2", "message": "status of TKT-001", "employee_id": "EMP001"},
            headers=auth_headers,
        )
    assert response.status_code == 200
    data = response.json()
    assert len(data["tools_used"]) == 1
    assert data["tools_used"][0]["tool_name"] == "get_ticket_status"


def test_ask_maintains_session_history(client, auth_headers):
    with patch("backend.api.routes.helpdesk.run_agent", return_value=("Reply 1", [])) as mock:
        client.post("/ask",
            json={"session_id": "test-s3", "message": "first message", "employee_id": "EMP001"},
            headers=auth_headers,
        )
        # Second call — check history was passed
        client.post("/ask",
            json={"session_id": "test-s3", "message": "second message", "employee_id": "EMP001"},
            headers=auth_headers,
        )
        # History passed to second call should contain first message
        second_call_history = mock.call_args[0][0]
        assert any(m["content"] == "first message" for m in second_call_history)


def test_delete_session(client, auth_headers):
    with patch("backend.api.routes.helpdesk.run_agent", return_value=("hi", [])):
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

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written: {path}")

print("\nAll test files written successfully.")