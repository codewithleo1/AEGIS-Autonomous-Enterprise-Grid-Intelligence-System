from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from backend.api.middleware.jwt_auth import get_current_user
from backend.services.ticket_service import list_tickets_async, update_ticket_async

router = APIRouter()


class TicketUpdateRequest(BaseModel):
    status: str
    note: str | None = None


@router.get("/tickets")
async def get_tickets(
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    category: str | None = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    """
    List tickets.
    - Employees see only their own tickets.
    - Agents see all tickets.
    """
    # Scope by employee ID if role is employee
    employee_id = None
    if current_user["role"] == "employee":
        employee_id = current_user["id"]

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
    current_user: dict = Depends(get_current_user),
):
    """Update ticket status. Agents only."""
    if current_user["role"] != "agent":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Agent access required.")

    return await update_ticket_async(
        ticket_id=ticket_id,
        status=body.status,
        note=body.note,
    )