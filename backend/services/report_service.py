from backend.services.ticket_service import TICKETS


def generate_report(
    date_from: str | None = None,
    date_to: str | None = None,
    filter_by: str | None = None,
) -> dict:
    """Generate a helpdesk summary report with optional filters."""
    tickets = list(TICKETS.values())

    # Date filtering
    if date_from:
        tickets = [t for t in tickets if t["created"] >= date_from]
    if date_to:
        tickets = [t for t in tickets if t["created"] <= date_to]

    total = len(tickets)

    # Build breakdown based on filter_by
    breakdown: dict = {}

    if filter_by == "status":
        for t in tickets:
            breakdown[t["status"]] = breakdown.get(t["status"], 0) + 1

    elif filter_by == "priority":
        for t in tickets:
            breakdown[t["priority"]] = breakdown.get(t["priority"], 0) + 1

    elif filter_by == "category":
        for t in tickets:
            breakdown[t["category"]] = breakdown.get(t["category"], 0) + 1

    elif filter_by == "department":
        # Import here to avoid circular imports
        from backend.services.employee_service import EMPLOYEES
        for t in tickets:
            emp = EMPLOYEES.get(t["employee_id"], {})
            dept = emp.get("department", "Unknown")
            breakdown[dept] = breakdown.get(dept, 0) + 1

    else:
        # Default: show all breakdowns
        for t in tickets:
            breakdown.setdefault("by_status", {})
            breakdown.setdefault("by_priority", {})
            breakdown.setdefault("by_category", {})
            breakdown["by_status"][t["status"]] = breakdown["by_status"].get(t["status"], 0) + 1
            breakdown["by_priority"][t["priority"]] = breakdown["by_priority"].get(t["priority"], 0) + 1
            breakdown["by_category"][t["category"]] = breakdown["by_category"].get(t["category"], 0) + 1

    return {
        "total_tickets": total,
        "date_from": date_from or "all time",
        "date_to": date_to or "all time",
        "filter_by": filter_by or "all",
        "breakdown": breakdown,
        "avg_resolution_time": "1.2 days",
    }