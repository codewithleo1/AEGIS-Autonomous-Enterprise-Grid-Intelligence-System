"""
Seed script — populates Supabase PostgreSQL with mock data.
Run once: uv run python seed.py
"""
import asyncio

from sqlalchemy import text

from backend.db.models import Agent, Employee, Ticket
from backend.db.postgres import AsyncSessionLocal, create_tables
from backend.logger import setup_logger
from backend.services.auth_service import hash_password

logger = setup_logger("seed")

# Default password for all users in development
DEFAULT_PASSWORD = hash_password("aegis1234")

EMPLOYEES = [
    Employee(employee_id="EMP001", name="Raj Sharma", department="Engineering", email="raj.sharma@techcorp.com", manager="EMP010", location="Mumbai", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP002", name="Priya Patel", department="Human Resources", email="priya.patel@techcorp.com", manager="EMP011", location="Bangalore", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP003", name="Amit Verma", department="Finance", email="amit.verma@techcorp.com", manager="EMP012", location="Delhi", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP004", name="Sneha Iyer", department="Marketing", email="sneha.iyer@techcorp.com", manager="EMP010", location="Mumbai", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP005", name="Rohan Mehta", department="Engineering", email="rohan.mehta@techcorp.com", manager="EMP010", location="Pune", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP006", name="Kavya Nair", department="Marketing", email="kavya.nair@techcorp.com", manager="EMP010", location="Mumbai", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP007", name="Arjun Das", department="Finance", email="arjun.das@techcorp.com", manager="EMP012", location="Delhi", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP008", name="Meera Joshi", department="Human Resources", email="meera.joshi@techcorp.com", manager="EMP011", location="Bangalore", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP009", name="Siddharth Rao", department="Engineering", email="siddharth.rao@techcorp.com", manager="EMP010", location="Pune", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP010", name="Vikram Nair", department="Engineering", email="vikram.nair@techcorp.com", manager="EMP020", location="Mumbai", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP011", name="Deepa Rao", department="HR Lead", email="deepa.rao@techcorp.com", manager="EMP020", location="Bangalore", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP012", name="Suresh Kumar", department="Finance Lead", email="suresh.k@techcorp.com", manager="EMP020", location="Delhi", password_hash=DEFAULT_PASSWORD),
    Employee(employee_id="EMP020", name="Anita Desai", department="CTO", email="anita.desai@techcorp.com", manager=None, location="Mumbai", password_hash=DEFAULT_PASSWORD),
]

AGENTS = [
    Agent(agent_id="AGT-001", name="Kiran Pillai", email="kiran.pillai@techcorp.com", specialisation="Hardware", password_hash=DEFAULT_PASSWORD),
    Agent(agent_id="AGT-002", name="Nisha Gupta", email="nisha.gupta@techcorp.com", specialisation="Software", password_hash=DEFAULT_PASSWORD),
    Agent(agent_id="AGT-003", name="Tarun Bose", email="tarun.bose@techcorp.com", specialisation="Network", password_hash=DEFAULT_PASSWORD),
    Agent(agent_id="AGT-004", name="Salma Shaikh", email="salma.shaikh@techcorp.com", specialisation="Authentication", password_hash=DEFAULT_PASSWORD),
    Agent(agent_id="AGT-005", name="Dev Malhotra", email="dev.malhotra@techcorp.com", specialisation="General / Other", password_hash=DEFAULT_PASSWORD),
]

TICKETS = [
    Ticket(ticket_id="TKT-001", title="WiFi not connecting", employee_id="EMP001", priority="HIGH", status="Open", category="Network", assigned_agent="AGT-003", assigned_agent_name="Tarun Bose", created="2025-07-01", updated="2025-07-01"),
    Ticket(ticket_id="TKT-002", title="Laptop won't boot", employee_id="EMP002", priority="CRITICAL", status="In Progress", category="Hardware", assigned_agent="AGT-001", assigned_agent_name="Kiran Pillai", created="2025-07-02", updated="2025-07-03"),
    Ticket(ticket_id="TKT-003", title="Cannot access Slack", employee_id="EMP003", priority="MEDIUM", status="Resolved", category="Software", assigned_agent="AGT-002", assigned_agent_name="Nisha Gupta", created="2025-07-03", updated="2025-07-04"),
    Ticket(ticket_id="TKT-004", title="Email login failing", employee_id="EMP004", priority="HIGH", status="Open", category="Authentication", assigned_agent="AGT-004", assigned_agent_name="Salma Shaikh", created="2025-07-05", updated="2025-07-05"),
    Ticket(ticket_id="TKT-005", title="Monitor display flickering", employee_id="EMP005", priority="LOW", status="Open", category="Hardware", assigned_agent="AGT-001", assigned_agent_name="Kiran Pillai", created="2025-07-06", updated="2025-07-06"),
    Ticket(ticket_id="TKT-006", title="VPN disconnects frequently", employee_id="EMP001", priority="HIGH", status="In Progress", category="Network", assigned_agent="AGT-003", assigned_agent_name="Tarun Bose", created="2025-07-07", updated="2025-07-08"),
    Ticket(ticket_id="TKT-007", title="Zoom audio not working", employee_id="EMP003", priority="MEDIUM", status="Open", category="Software", assigned_agent="AGT-002", assigned_agent_name="Nisha Gupta", created="2025-07-09", updated="2025-07-09"),
    Ticket(ticket_id="TKT-008", title="Printer not recognized", employee_id="EMP002", priority="LOW", status="Resolved", category="Hardware", assigned_agent="AGT-001", assigned_agent_name="Kiran Pillai", created="2025-07-10", updated="2025-07-11"),
    Ticket(ticket_id="TKT-009", title="Two-factor auth app not syncing", employee_id="EMP006", priority="HIGH", status="Open", category="Authentication", assigned_agent="AGT-004", assigned_agent_name="Salma Shaikh", created="2025-07-10", updated="2025-07-10"),
    Ticket(ticket_id="TKT-010", title="Excel crashes on large files", employee_id="EMP007", priority="MEDIUM", status="In Progress", category="Software", assigned_agent="AGT-002", assigned_agent_name="Nisha Gupta", created="2025-07-10", updated="2025-07-11"),
    Ticket(ticket_id="TKT-011", title="Office network very slow", employee_id="EMP008", priority="HIGH", status="Open", category="Network", assigned_agent="AGT-003", assigned_agent_name="Tarun Bose", created="2025-07-11", updated="2025-07-11"),
    Ticket(ticket_id="TKT-012", title="Keyboard unresponsive", employee_id="EMP009", priority="LOW", status="Resolved", category="Hardware", assigned_agent="AGT-001", assigned_agent_name="Kiran Pillai", created="2025-07-11", updated="2025-07-12"),
    Ticket(ticket_id="TKT-013", title="Cannot install VS Code", employee_id="EMP005", priority="MEDIUM", status="Open", category="Software", assigned_agent="AGT-002", assigned_agent_name="Nisha Gupta", created="2025-07-12", updated="2025-07-12"),
    Ticket(ticket_id="TKT-014", title="SSO login broken after update", employee_id="EMP003", priority="CRITICAL", status="In Progress", category="Authentication", assigned_agent="AGT-004", assigned_agent_name="Salma Shaikh", created="2025-07-12", updated="2025-07-13"),
    Ticket(ticket_id="TKT-015", title="External hard drive not detected", employee_id="EMP004", priority="LOW", status="Open", category="Hardware", assigned_agent="AGT-001", assigned_agent_name="Kiran Pillai", created="2025-07-12", updated="2025-07-12"),
    Ticket(ticket_id="TKT-016", title="Video conferencing lag", employee_id="EMP010", priority="MEDIUM", status="Open", category="Network", assigned_agent="AGT-003", assigned_agent_name="Tarun Bose", created="2025-07-13", updated="2025-07-13"),
    Ticket(ticket_id="TKT-017", title="Antivirus flagging internal tool", employee_id="EMP010", priority="HIGH", status="Open", category="Software", assigned_agent="AGT-002", assigned_agent_name="Nisha Gupta", created="2025-07-13", updated="2025-07-13"),
    Ticket(ticket_id="TKT-018", title="New laptop setup required", employee_id="EMP006", priority="MEDIUM", status="In Progress", category="Hardware", assigned_agent="AGT-005", assigned_agent_name="Dev Malhotra", created="2025-07-13", updated="2025-07-14"),
    Ticket(ticket_id="TKT-019", title="Access to HR portal denied", employee_id="EMP007", priority="HIGH", status="Open", category="Authentication", assigned_agent="AGT-004", assigned_agent_name="Salma Shaikh", created="2025-07-14", updated="2025-07-14"),
    Ticket(ticket_id="TKT-020", title="Mouse scroll not working", employee_id="EMP008", priority="LOW", status="Open", category="Hardware", assigned_agent="AGT-001", assigned_agent_name="Kiran Pillai", created="2025-07-14", updated="2025-07-14"),
]


async def seed():
    await create_tables()

    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM tickets"))
        await session.execute(text("DELETE FROM agents"))
        await session.execute(text("DELETE FROM employees"))
        await session.commit()
        logger.info("Cleared existing data")

        # Insert in order: top-level first, then reports
        ordered = [
            next(e for e in EMPLOYEES if e.employee_id == "EMP020"),  # CTO
            next(e for e in EMPLOYEES if e.employee_id == "EMP010"),  # Eng Lead
            next(e for e in EMPLOYEES if e.employee_id == "EMP011"),  # HR Lead
            next(e for e in EMPLOYEES if e.employee_id == "EMP012"),  # Finance Lead
            *[e for e in EMPLOYEES if e.employee_id not in {"EMP020", "EMP010", "EMP011", "EMP012"}],
        ]
        for emp in ordered:
            session.add(emp)
        await session.commit()
        logger.info("Seeded %d employees", len(EMPLOYEES))

        for agent in AGENTS:
            session.add(agent)
        await session.commit()
        logger.info("Seeded %d agents", len(AGENTS))

        for ticket in TICKETS:
            session.add(ticket)
        await session.commit()
        logger.info("Seeded %d tickets", len(TICKETS))

    logger.info("Seed complete")
    logger.info("Default password for all users: aegis1234")


if __name__ == "__main__":
    asyncio.run(seed())