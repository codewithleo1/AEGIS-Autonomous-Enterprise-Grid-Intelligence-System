from fastapi import APIRouter, Query
from pydantic import BaseModel

from backend.services.ticket_service import list_tickets_async, update_ticket_async

router = APIRouter()


class TicketUpdateRequest(BaseModel):
    status: str
    note: str | None = None


@router.get("/tickets")
async def get_tickets(
    employee_id: str | None = Query(default=None, description="Filter by employee ID"),
    status: str | None = Query(default=None, description="Filter by status"),
    priority: str | None = Query(default=None, description="Filter by priority"),
    category: str | None = Query(default=None, description="Filter by category"),
):
    """List tickets with optional filters. Used by the frontend dashboard."""
    return await list_tickets_async(
        employee_id=employee_id,
        status=status,
        priority=priority,
        category=category,
    )


@router.patch("/tickets/{ticket_id}")
async def patch_ticket(
    ticket_id: str,
    body: TicketUpdateRequest,
):
    """Update ticket status. Used by the agent dashboard."""
    return await update_ticket_async(
        ticket_id=ticket_id,
        status=body.status,
        note=body.note,
    )