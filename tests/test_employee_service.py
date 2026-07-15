import asyncio
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
