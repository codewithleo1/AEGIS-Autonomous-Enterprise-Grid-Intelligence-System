from fastapi import APIRouter, Query

from backend.services.ticket_service import list_tickets

router = APIRouter()


@router.get("/tickets")
async def get_tickets(
    employee_id: str | None = Query(default=None, description="Filter by employee ID"),
    status: str | None = Query(default=None, description="Filter by status"),
    priority: str | None = Query(default=None, description="Filter by priority"),
    category: str | None = Query(default=None, description="Filter by category"),
):
    """List tickets with optional filters. Used by the frontend dashboard."""
    return list_tickets(
        employee_id=employee_id,
        status=status,
        priority=priority,
        category=category,
    )