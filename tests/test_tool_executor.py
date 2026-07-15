# test_tool_executor.py
import asyncio
from unittest.mock import AsyncMock, patch

from backend.agent.tool_executor import execute_tool


def test_execute_known_tool():
    with patch("backend.services.ticket_service.get_ticket_status_async", new_callable=AsyncMock, return_value={"ticket_id": "TKT-001", "status": "Open"}):
        result = asyncio.run(execute_tool("get_ticket_status", {"ticket_id": "TKT-001"}))
    assert result["ticket_id"] == "TKT-001"


def test_execute_unknown_tool_returns_error():
    result = asyncio.run(execute_tool("nonexistent_tool", {}))
    assert "error" in result
    assert "Unknown tool" in result["error"]


def test_execute_get_employee_info():
    with patch("backend.services.employee_service.get_employee_info_async", new_callable=AsyncMock, return_value={"name": "Raj Sharma", "employee_id": "EMP001"}):
        result = asyncio.run(execute_tool("get_employee_info", {"employee_id": "EMP001"}))
    assert result["name"] == "Raj Sharma"


def test_execute_list_tickets():
    with patch("backend.services.ticket_service.list_tickets_async", new_callable=AsyncMock, return_value={"total": 5, "tickets": []}):
        result = asyncio.run(execute_tool("list_tickets", {"status": "Open"}))
    assert result["total"] == 5


def test_execute_tool_handles_exception_gracefully():
    with patch("backend.services.ticket_service.get_ticket_status_async", new_callable=AsyncMock, side_effect=Exception("DB error")):
        result = asyncio.run(execute_tool("get_ticket_status", {"ticket_id": "TKT-001"}))
    assert "error" in result


def test_execute_create_ticket():
    with patch("backend.services.ticket_service.create_ticket_async", new_callable=AsyncMock, return_value={"ticket_id": "TKT-021", "status": "Open"}):
        result = asyncio.run(execute_tool("create_ticket", {
            "employee_id": "EMP001", "title": "Test",
            "priority": "LOW", "category": "Other", "description": "Test",
        }))
    assert result["ticket_id"] == "TKT-021"