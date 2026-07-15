import asyncio
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
