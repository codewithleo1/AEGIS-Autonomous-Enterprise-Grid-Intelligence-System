from unittest.mock import patch
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
