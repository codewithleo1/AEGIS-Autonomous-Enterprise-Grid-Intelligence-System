files = {}

files["tests/test_employee_service.py"] = """from unittest.mock import AsyncMock, patch


def test_get_existing_employee():
    mock_emp = AsyncMock()
    mock_emp.employee_id = "EMP001"
    mock_emp.name = "Raj Sharma"
    mock_emp.department = "Engineering"
    mock_emp.email = "raj.sharma@techcorp.com"
    mock_emp.manager = "EMP010"
    mock_emp.location = "Mumbai"

    with patch("backend.services.employee_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_emp
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        import asyncio
        from backend.services.employee_service import get_employee_info_async
        result = asyncio.run(get_employee_info_async("EMP001"))

    assert result["name"] == "Raj Sharma"
    assert result["department"] == "Engineering"
    assert result["employee_id"] == "EMP001"


def test_get_nonexistent_employee_returns_error():
    with patch("backend.services.employee_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        import asyncio
        from backend.services.employee_service import get_employee_info_async
        result = asyncio.run(get_employee_info_async("EMP999"))

    assert "error" in result


def test_get_employee_case_insensitive():
    mock_emp = AsyncMock()
    mock_emp.employee_id = "EMP001"
    mock_emp.name = "Raj Sharma"
    mock_emp.department = "Engineering"
    mock_emp.email = "raj.sharma@techcorp.com"
    mock_emp.manager = "EMP010"
    mock_emp.location = "Mumbai"

    with patch("backend.services.employee_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_emp
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        import asyncio
        from backend.services.employee_service import get_employee_info_async
        result = asyncio.run(get_employee_info_async("emp001"))

    assert result["name"] == "Raj Sharma"
"""

files["tests/test_ticket_service.py"] = """import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


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
    mock_ticket = make_mock_ticket()

    with patch("backend.services.ticket_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_ticket
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.ticket_service import get_ticket_status_async
        result = asyncio.run(get_ticket_status_async("TKT-001"))

    assert result["ticket_id"] == "TKT-001"
    assert result["status"] == "Open"
    assert result["priority"] == "HIGH"


def test_get_nonexistent_ticket_returns_error():
    with patch("backend.services.ticket_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.ticket_service import get_ticket_status_async
        result = asyncio.run(get_ticket_status_async("TKT-999"))

    assert "error" in result


def test_list_tickets_returns_results():
    mock_ticket = make_mock_ticket()

    with patch("backend.services.ticket_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = [mock_ticket]
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.ticket_service import list_tickets_async
        result = asyncio.run(list_tickets_async())

    assert result["total"] == 1
    assert result["tickets"][0]["ticket_id"] == "TKT-001"


def test_update_ticket_status():
    mock_ticket = make_mock_ticket()

    with patch("backend.services.ticket_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_ticket
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.ticket_service import update_ticket_async
        result = asyncio.run(update_ticket_async("TKT-001", "Resolved", "Fixed the issue"))

    assert result["new_status"] == "Resolved"
    assert result["note"] == "Fixed the issue"


def test_update_nonexistent_ticket_returns_error():
    with patch("backend.services.ticket_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.ticket_service import update_ticket_async
        result = asyncio.run(update_ticket_async("TKT-999", "Resolved"))

    assert "error" in result


def test_create_ticket_assigns_correct_agent():
    with patch("backend.services.ticket_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_count_result = AsyncMock()
        mock_count_result.scalar.return_value = 20
        mock_ctx.execute = AsyncMock(return_value=mock_count_result)
        mock_ctx.add = MagicMock()
        mock_ctx.commit = AsyncMock()

        from backend.services.ticket_service import create_ticket_async
        result = asyncio.run(create_ticket_async(
            employee_id="EMP001",
            title="Test issue",
            priority="HIGH",
            category="Network",
            description="Test",
        ))

    assert result["assigned_agent_name"] == "Tarun Bose"
    assert result["status"] == "Open"
    assert result["ticket_id"] == "TKT-021"
"""

files["tests/test_report_service.py"] = """import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


def make_mock_tickets():
    tickets = []
    statuses = ["Open", "Open", "Resolved", "In Progress"]
    priorities = ["HIGH", "CRITICAL", "MEDIUM", "LOW"]
    categories = ["Network", "Hardware", "Software", "Authentication"]
    for i, (s, p, c) in enumerate(zip(statuses, priorities, categories)):
        t = MagicMock()
        t.ticket_id = f"TKT-00{i+1}"
        t.status = s
        t.priority = p
        t.category = c
        t.employee_id = "EMP001"
        t.created = "2025-07-01"
        tickets.append(t)
    return tickets


def test_report_returns_required_fields():
    with patch("backend.services.report_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = make_mock_tickets()
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async())

    assert "total_tickets" in result
    assert "breakdown" in result
    assert "avg_resolution_time" in result


def test_report_filter_by_status():
    with patch("backend.services.report_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = make_mock_tickets()
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async(filter_by="status"))

    assert "Open" in result["breakdown"]


def test_report_filter_by_priority():
    with patch("backend.services.report_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = make_mock_tickets()
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async(filter_by="priority"))

    assert "HIGH" in result["breakdown"]


def test_report_filter_by_category():
    with patch("backend.services.report_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = make_mock_tickets()
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async(filter_by="category"))

    assert "Network" in result["breakdown"]


def test_report_total_matches_mock():
    with patch("backend.services.report_service.AsyncSessionLocal") as mock_session:
        mock_ctx = AsyncMock()
        mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_ctx)
        mock_session.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = make_mock_tickets()
        mock_ctx.execute = AsyncMock(return_value=mock_result)

        from backend.services.report_service import generate_report_async
        result = asyncio.run(generate_report_async())

    assert result["total_tickets"] == 4
"""

files["tests/test_tool_executor.py"] = """import asyncio
from unittest.mock import AsyncMock, patch


def test_execute_known_tool():
    with patch("backend.agent.tool_executor.get_ticket_status_async", new_callable=AsyncMock) as mock_fn:
        mock_fn.return_value = {"ticket_id": "TKT-001", "status": "Open"}
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("get_ticket_status", {"ticket_id": "TKT-001"}))
    assert result["ticket_id"] == "TKT-001"


def test_execute_unknown_tool_returns_error():
    from backend.agent.tool_executor import execute_tool
    result = asyncio.run(execute_tool("nonexistent_tool", {}))
    assert "error" in result
    assert "Unknown tool" in result["error"]


def test_execute_get_employee_info():
    with patch("backend.agent.tool_executor.get_employee_info_async", new_callable=AsyncMock) as mock_fn:
        mock_fn.return_value = {"name": "Raj Sharma", "employee_id": "EMP001"}
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("get_employee_info", {"employee_id": "EMP001"}))
    assert result["name"] == "Raj Sharma"


def test_execute_list_tickets():
    with patch("backend.agent.tool_executor.list_tickets_async", new_callable=AsyncMock) as mock_fn:
        mock_fn.return_value = {"total": 5, "tickets": []}
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("list_tickets", {"status": "Open"}))
    assert result["total"] == 5


def test_execute_tool_handles_exception_gracefully():
    with patch("backend.agent.tool_executor.get_ticket_status_async", new_callable=AsyncMock) as mock_fn:
        mock_fn.side_effect = Exception("DB connection failed")
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("get_ticket_status", {"ticket_id": "TKT-001"}))
    assert "error" in result


def test_execute_create_ticket():
    with patch("backend.agent.tool_executor.create_ticket_async", new_callable=AsyncMock) as mock_fn:
        mock_fn.return_value = {"ticket_id": "TKT-021", "status": "Open"}
        from backend.agent.tool_executor import execute_tool
        result = asyncio.run(execute_tool("create_ticket", {
            "employee_id": "EMP001",
            "title": "Test",
            "priority": "LOW",
            "category": "Other",
            "description": "Test",
        }))
    assert result["ticket_id"] == "TKT-021"
"""

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written: {path}")

print("\nAll test files written successfully.")