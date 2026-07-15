from datetime import datetime

# Mock ticket data — mirrors mock-database.md
# Will be replaced with real DB queries in Step 17

TICKETS: dict[str, dict] = {
    "TKT-001": {"ticket_id": "TKT-001", "title": "WiFi not connecting", "employee_id": "EMP001", "priority": "HIGH", "status": "Open", "category": "Network", "assigned_agent": "AGT-003", "assigned_agent_name": "Tarun Bose", "created": "2025-07-01", "updated": "2025-07-01"},
    "TKT-002": {"ticket_id": "TKT-002", "title": "Laptop won't boot", "employee_id": "EMP002", "priority": "CRITICAL", "status": "In Progress", "category": "Hardware", "assigned_agent": "AGT-001", "assigned_agent_name": "Kiran Pillai", "created": "2025-07-02", "updated": "2025-07-03"},
    "TKT-003": {"ticket_id": "TKT-003", "title": "Cannot access Slack", "employee_id": "EMP003", "priority": "MEDIUM", "status": "Resolved", "category": "Software", "assigned_agent": "AGT-002", "assigned_agent_name": "Nisha Gupta", "created": "2025-07-03", "updated": "2025-07-04"},
    "TKT-004": {"ticket_id": "TKT-004", "title": "Email login failing", "employee_id": "EMP004", "priority": "HIGH", "status": "Open", "category": "Authentication", "assigned_agent": "AGT-004", "assigned_agent_name": "Salma Shaikh", "created": "2025-07-05", "updated": "2025-07-05"},
    "TKT-005": {"ticket_id": "TKT-005", "title": "Monitor display flickering", "employee_id": "EMP005", "priority": "LOW", "status": "Open", "category": "Hardware", "assigned_agent": "AGT-001", "assigned_agent_name": "Kiran Pillai", "created": "2025-07-06", "updated": "2025-07-06"},
    "TKT-006": {"ticket_id": "TKT-006", "title": "VPN disconnects frequently", "employee_id": "EMP001", "priority": "HIGH", "status": "In Progress", "category": "Network", "assigned_agent": "AGT-003", "assigned_agent_name": "Tarun Bose", "created": "2025-07-07", "updated": "2025-07-08"},
    "TKT-007": {"ticket_id": "TKT-007", "title": "Zoom audio not working", "employee_id": "EMP003", "priority": "MEDIUM", "status": "Open", "category": "Software", "assigned_agent": "AGT-002", "assigned_agent_name": "Nisha Gupta", "created": "2025-07-09", "updated": "2025-07-09"},
    "TKT-008": {"ticket_id": "TKT-008", "title": "Printer not recognized", "employee_id": "EMP002", "priority": "LOW", "status": "Resolved", "category": "Hardware", "assigned_agent": "AGT-001", "assigned_agent_name": "Kiran Pillai", "created": "2025-07-10", "updated": "2025-07-11"},
    "TKT-009": {"ticket_id": "TKT-009", "title": "Two-factor auth app not syncing", "employee_id": "EMP006", "priority": "HIGH", "status": "Open", "category": "Authentication", "assigned_agent": "AGT-004", "assigned_agent_name": "Salma Shaikh", "created": "2025-07-10", "updated": "2025-07-10"},
    "TKT-010": {"ticket_id": "TKT-010", "title": "Excel crashes on large files", "employee_id": "EMP007", "priority": "MEDIUM", "status": "In Progress", "category": "Software", "assigned_agent": "AGT-002", "assigned_agent_name": "Nisha Gupta", "created": "2025-07-10", "updated": "2025-07-11"},
    "TKT-011": {"ticket_id": "TKT-011", "title": "Office network very slow", "employee_id": "EMP008", "priority": "HIGH", "status": "Open", "category": "Network", "assigned_agent": "AGT-003", "assigned_agent_name": "Tarun Bose", "created": "2025-07-11", "updated": "2025-07-11"},
    "TKT-012": {"ticket_id": "TKT-012", "title": "Keyboard unresponsive", "employee_id": "EMP009", "priority": "LOW", "status": "Resolved", "category": "Hardware", "assigned_agent": "AGT-001", "assigned_agent_name": "Kiran Pillai", "created": "2025-07-11", "updated": "2025-07-12"},
    "TKT-013": {"ticket_id": "TKT-013", "title": "Cannot install VS Code", "employee_id": "EMP005", "priority": "MEDIUM", "status": "Open", "category": "Software", "assigned_agent": "AGT-002", "assigned_agent_name": "Nisha Gupta", "created": "2025-07-12", "updated": "2025-07-12"},
    "TKT-014": {"ticket_id": "TKT-014", "title": "SSO login broken after update", "employee_id": "EMP003", "priority": "CRITICAL", "status": "In Progress", "category": "Authentication", "assigned_agent": "AGT-004", "assigned_agent_name": "Salma Shaikh", "created": "2025-07-12", "updated": "2025-07-13"},
    "TKT-015": {"ticket_id": "TKT-015", "title": "External hard drive not detected", "employee_id": "EMP004", "priority": "LOW", "status": "Open", "category": "Hardware", "assigned_agent": "AGT-001", "assigned_agent_name": "Kiran Pillai", "created": "2025-07-12", "updated": "2025-07-12"},
    "TKT-016": {"ticket_id": "TKT-016", "title": "Video conferencing lag", "employee_id": "EMP010", "priority": "MEDIUM", "status": "Open", "category": "Network", "assigned_agent": "AGT-003", "assigned_agent_name": "Tarun Bose", "created": "2025-07-13", "updated": "2025-07-13"},
    "TKT-017": {"ticket_id": "TKT-017", "title": "Antivirus flagging internal tool", "employee_id": "EMP010", "priority": "HIGH", "status": "Open", "category": "Software", "assigned_agent": "AGT-002", "assigned_agent_name": "Nisha Gupta", "created": "2025-07-13", "updated": "2025-07-13"},
    "TKT-018": {"ticket_id": "TKT-018", "title": "New laptop setup required", "employee_id": "EMP006", "priority": "MEDIUM", "status": "In Progress", "category": "Hardware", "assigned_agent": "AGT-005", "assigned_agent_name": "Dev Malhotra", "created": "2025-07-13", "updated": "2025-07-14"},
    "TKT-019": {"ticket_id": "TKT-019", "title": "Access to HR portal denied", "employee_id": "EMP007", "priority": "HIGH", "status": "Open", "category": "Authentication", "assigned_agent": "AGT-004", "assigned_agent_name": "Salma Shaikh", "created": "2025-07-14", "updated": "2025-07-14"},
    "TKT-020": {"ticket_id": "TKT-020", "title": "Mouse scroll not working", "employee_id": "EMP008", "priority": "LOW", "status": "Open", "category": "Hardware", "assigned_agent": "AGT-001", "assigned_agent_name": "Kiran Pillai", "created": "2025-07-14", "updated": "2025-07-14"},
}

# Agent pool for auto-assignment based on category
AGENT_POOL = {
    "Hardware": {"agent_id": "AGT-001", "name": "Kiran Pillai"},
    "Software": {"agent_id": "AGT-002", "name": "Nisha Gupta"},
    "Network":  {"agent_id": "AGT-003", "name": "Tarun Bose"},
    "Authentication": {"agent_id": "AGT-004", "name": "Salma Shaikh"},
    "Other":    {"agent_id": "AGT-005", "name": "Dev Malhotra"},
}

# Track next ticket number
_next_ticket_num = 21


def create_ticket(
    employee_id: str,
    title: str,
    priority: str,
    category: str,
    description: str,
) -> dict:
    """Create a new IT support ticket and auto-assign an agent."""
    global _next_ticket_num

    agent = AGENT_POOL.get(category, AGENT_POOL["Other"])
    ticket_id = f"TKT-{_next_ticket_num:03d}"
    now = datetime.now().strftime("%Y-%m-%d")

    ticket = {
        "ticket_id": ticket_id,
        "title": title,
        "employee_id": employee_id.upper(),
        "priority": priority,
        "status": "Open",
        "category": category,
        "description": description,
        "assigned_agent": agent["agent_id"],
        "assigned_agent_name": agent["name"],
        "created": now,
        "updated": now,
    }

    TICKETS[ticket_id] = ticket
    _next_ticket_num += 1
    return ticket


def get_ticket_status(ticket_id: str) -> dict:
    """Get the current status of a ticket."""
    ticket = TICKETS.get(ticket_id.upper())
    if not ticket:
        return {"error": f"Ticket {ticket_id} not found. Please check the ID."}
    return ticket


def list_tickets(
    employee_id: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    category: str | None = None,
) -> dict:
    """List tickets with optional filters."""
    results = list(TICKETS.values())

    if employee_id:
        results = [t for t in results if t["employee_id"] == employee_id.upper()]
    if status:
        results = [t for t in results if t["status"] == status]
    if priority:
        results = [t for t in results if t["priority"] == priority]
    if category:
        results = [t for t in results if t["category"] == category]

    return {"total": len(results), "tickets": results}


def update_ticket(ticket_id: str, status: str, note: str | None = None) -> dict:
    """Update a ticket's status and optionally add a resolution note."""
    ticket = TICKETS.get(ticket_id.upper())
    if not ticket:
        return {"error": f"Ticket {ticket_id} not found. Please check the ID."}

    old_status = ticket["status"]
    ticket["status"] = status
    ticket["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    if note:
        ticket["resolution_note"] = note

    return {
        "ticket_id": ticket_id,
        "title": ticket["title"],
        "old_status": old_status,
        "new_status": status,
        "note": note or "",
        "updated_at": ticket["updated"],
    }