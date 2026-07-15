TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": (
                "Create a new IT support ticket for a TechCorp employee. "
                "Always verify the employee_id and confirm title + priority "
                "with the user before calling this tool."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "TechCorp employee ID e.g. EMP001",
                    },
                    "title": {
                        "type": "string",
                        "description": "Short description of the issue",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                        "description": "Ticket priority level",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Hardware", "Software", "Network", "Authentication", "Other"],
                        "description": "Type of IT issue",
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed explanation of the problem",
                    },
                },
                "required": ["employee_id", "title", "priority", "category", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket_status",
            "description": "Check the current status of an existing IT support ticket by ticket ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "Ticket ID e.g. TKT-001",
                    },
                },
                "required": ["ticket_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tickets",
            "description": (
                "List IT support tickets with optional filters. "
                "Can filter by employee, status, priority, or category."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "Filter tickets by employee ID",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["Open", "In Progress", "Resolved"],
                        "description": "Filter by ticket status",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                        "description": "Filter by priority level",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["Hardware", "Software", "Network", "Authentication", "Other"],
                        "description": "Filter by issue category",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_employee_info",
            "description": "Look up a TechCorp employee's profile by their Employee ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "TechCorp employee ID e.g. EMP001",
                    },
                },
                "required": ["employee_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_ticket",
            "description": (
                "Update the status of an existing ticket or add a resolution note. "
                "Always confirm ticket_id and new status with user before calling. "
                "Always ask for a resolution note when setting status to Resolved."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "Ticket ID to update e.g. TKT-005",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["Open", "In Progress", "Resolved"],
                        "description": "New status for the ticket",
                    },
                    "note": {
                        "type": "string",
                        "description": "Optional resolution note or update message",
                    },
                },
                "required": ["ticket_id", "status"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_report",
            "description": (
                "Generate a helpdesk activity summary report. "
                "Ask for date range and filter type if not provided."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "date_from": {
                        "type": "string",
                        "description": "Start date e.g. 2025-07-01",
                    },
                    "date_to": {
                        "type": "string",
                        "description": "End date e.g. 2025-07-14",
                    },
                    "filter_by": {
                        "type": "string",
                        "enum": ["department", "priority", "category", "status"],
                        "description": "How to break down the report",
                    },
                },
                "required": [],
            },
        },
    },
]