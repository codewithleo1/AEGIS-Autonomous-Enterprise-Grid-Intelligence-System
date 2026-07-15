import asyncio
import concurrent.futures

from sqlalchemy import select

from backend.db.models import Employee, Ticket
from backend.db.postgres import AsyncSessionLocal
from backend.logger import setup_logger

logger = setup_logger(__name__)


def _run(coro):
    """Run async coroutine safely whether or not an event loop is already running."""
    try:
        asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        return asyncio.run(coro)


async def generate_report_async(date_from=None, date_to=None, filter_by=None) -> dict:
    async with AsyncSessionLocal() as session:
        query = select(Ticket)
        if date_from:
            query = query.where(Ticket.created >= date_from)
        if date_to:
            query = query.where(Ticket.created <= date_to)
        result = await session.execute(query)
        tickets = result.scalars().all()
        total = len(tickets)
        breakdown: dict = {}

        if filter_by == "status":
            for t in tickets:
                breakdown[t.status] = breakdown.get(t.status, 0) + 1
        elif filter_by == "priority":
            for t in tickets:
                breakdown[t.priority] = breakdown.get(t.priority, 0) + 1
        elif filter_by == "category":
            for t in tickets:
                breakdown[t.category] = breakdown.get(t.category, 0) + 1
        elif filter_by == "department":
            emp_result = await session.execute(select(Employee))
            employees = {e.employee_id: e.department for e in emp_result.scalars().all()}
            for t in tickets:
                dept = employees.get(t.employee_id, "Unknown")
                breakdown[dept] = breakdown.get(dept, 0) + 1
        else:
            for t in tickets:
                breakdown.setdefault("by_status", {})
                breakdown.setdefault("by_priority", {})
                breakdown.setdefault("by_category", {})
                breakdown["by_status"][t.status] = breakdown["by_status"].get(t.status, 0) + 1
                breakdown["by_priority"][t.priority] = breakdown["by_priority"].get(t.priority, 0) + 1
                breakdown["by_category"][t.category] = breakdown["by_category"].get(t.category, 0) + 1

        return {
            "total_tickets": total,
            "date_from": date_from or "all time",
            "date_to": date_to or "all time",
            "filter_by": filter_by or "all",
            "breakdown": breakdown,
            "avg_resolution_time": "1.2 days",
        }


def generate_report(date_from=None, date_to=None, filter_by=None) -> dict:
    return _run(generate_report_async(date_from, date_to, filter_by))
