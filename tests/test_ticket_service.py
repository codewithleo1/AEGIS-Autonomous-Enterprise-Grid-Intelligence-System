import pytest
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
