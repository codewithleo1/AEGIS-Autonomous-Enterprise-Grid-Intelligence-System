from fastapi import APIRouter, HTTPException, Request

from backend.agent.groq_client import run_agent
from backend.api.middleware.rate_limit import limiter
from backend.db.redis_session import delete_session, load_session, save_session
from backend.schemas.request import AskRequest
from backend.schemas.response import AskResponse

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
@limiter.limit("30/minute")
async def ask(request: Request, body: AskRequest):
    session_id = body.session_id
    history = load_session(session_id)
    reply, tools_used = await run_agent(
        history=history,
        new_message=body.message,
        employee_id=body.employee_id or "UNKNOWN",
    )
    history.append({"role": "user", "content": body.message})
    history.append({"role": "assistant", "content": reply})
    save_session(session_id, history)
    return AskResponse(session_id=session_id, reply=reply, tools_used=tools_used)


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    deleted = delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": f"Session {session_id} cleared successfully"}