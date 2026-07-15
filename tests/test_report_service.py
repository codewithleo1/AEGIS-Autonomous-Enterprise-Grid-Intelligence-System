from backend.services.report_service import generate_report


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
