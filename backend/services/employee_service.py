import asyncio
import concurrent.futures

from sqlalchemy import select

from backend.db.models import Employee
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


async def get_employee_info_async(employee_id: str) -> dict:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Employee).where(Employee.employee_id == employee_id.upper())
        )
        employee = result.scalar_one_or_none()
        if not employee:
            return {"error": f"Employee {employee_id} not found. Please verify the ID."}
        return {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department": employee.department,
            "email": employee.email,
            "manager": employee.manager,
            "location": employee.location,
        }


def get_employee_info(employee_id: str) -> dict:
    return _run(get_employee_info_async(employee_id))
