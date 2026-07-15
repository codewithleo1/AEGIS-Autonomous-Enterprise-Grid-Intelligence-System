import asyncio
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
