import asyncio
import concurrent.futures
from datetime import datetime

from sqlalchemy import func, select

from backend.db.models import Ticket
from backend.db.postgres import AsyncSessionLocal
from backend.logger import setup_logger

logger = setup_logger(__name__)

AGENT_POOL = {
    "Hardware": {"agent_id": "AGT-001", "name": "Kiran Pillai"},
    "Software": {"agent_id": "AGT-002", "name": "Nisha Gupta"},
    "Network": {"agent_id": "AGT-003", "name": "Tarun Bose"},
    "Authentication": {"agent_id": "AGT-004", "name": "Salma Shaikh"},
    "Other": {"agent_id": "AGT-005", "name": "Dev Malhotra"},
}


def _run(coro):
    """Run async coroutine safely whether or not an event loop is already running."""
    try:
        asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        return asyncio.run(coro)


async def _get_next_ticket_id(session) -> str:
    result = await session.execute(select(func.count()).select_from(Ticket))
    count = result.scalar() or 0
    return f"TKT-{count + 1:03d}"


async def create_ticket_async(employee_id: str, title: str, priority: str, category: str, description: str) -> dict:
    agent = AGENT_POOL.get(category, AGENT_POOL["Other"])
    now = datetime.now().strftime("%Y-%m-%d")
    async with AsyncSessionLocal() as session:
        ticket_id = await _get_next_ticket_id(session)
        ticket = Ticket(
            ticket_id=ticket_id,
            title=title,
            employee_id=employee_id.upper(),
            priority=priority,
            status="Open",
            category=category,
            description=description,
            assigned_agent=agent["agent_id"],
            assigned_agent_name=agent["name"],
            created=now,
            updated=now,
        )
        session.add(ticket)
        await session.commit()
        return {
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


async def get_ticket_status_async(ticket_id: str) -> dict:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ticket).where(Ticket.ticket_id == ticket_id.upper())
        )
        ticket = result.scalar_one_or_none()
        if not ticket:
            return {"error": f"Ticket {ticket_id} not found. Please check the ID."}
        return {
            "ticket_id": ticket.ticket_id,
            "title": ticket.title,
            "employee_id": ticket.employee_id,
            "priority": ticket.priority,
            "status": ticket.status,
            "category": ticket.category,
            "assigned_agent": ticket.assigned_agent,
            "assigned_agent_name": ticket.assigned_agent_name,
            "created": ticket.created,
            "updated": ticket.updated,
        }


async def list_tickets_async(employee_id=None, status=None, priority=None, category=None) -> dict:
    async with AsyncSessionLocal() as session:
        query = select(Ticket)
        if employee_id:
            query = query.where(Ticket.employee_id == employee_id.upper())
        if status:
            query = query.where(Ticket.status == status)
        if priority:
            query = query.where(Ticket.priority == priority)
        if category:
            query = query.where(Ticket.category == category)
        result = await session.execute(query)
        tickets = result.scalars().all()
        return {
            "total": len(tickets),
            "tickets": [
                {
                    "ticket_id": t.ticket_id,
                    "title": t.title,
                    "employee_id": t.employee_id,
                    "priority": t.priority,
                    "status": t.status,
                    "category": t.category,
                    "assigned_agent": t.assigned_agent,
                    "assigned_agent_name": t.assigned_agent_name,
                    "created": t.created,
                    "updated": t.updated,
                }
                for t in tickets
            ],
        }


async def update_ticket_async(ticket_id: str, status: str, note: str | None = None) -> dict:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ticket).where(Ticket.ticket_id == ticket_id.upper())
        )
        ticket = result.scalar_one_or_none()
        if not ticket:
            return {"error": f"Ticket {ticket_id} not found. Please check the ID."}
        old_status = ticket.status
        ticket.status = status
        ticket.updated = datetime.now().strftime("%Y-%m-%d %H:%M")
        if note:
            ticket.resolution_note = note
        await session.commit()
        return {
            "ticket_id": ticket_id,
            "title": ticket.title,
            "old_status": old_status,
            "new_status": status,
            "note": note or "",
            "updated_at": ticket.updated,
        }


def create_ticket(employee_id: str, title: str, priority: str, category: str, description: str) -> dict:
    return _run(create_ticket_async(employee_id, title, priority, category, description))


def get_ticket_status(ticket_id: str) -> dict:
    return _run(get_ticket_status_async(ticket_id))


def list_tickets(employee_id=None, status=None, priority=None, category=None) -> dict:
    return _run(list_tickets_async(employee_id, status, priority, category))


def update_ticket(ticket_id: str, status: str, note: str | None = None) -> dict:
    return _run(update_ticket_async(ticket_id, status, note))
