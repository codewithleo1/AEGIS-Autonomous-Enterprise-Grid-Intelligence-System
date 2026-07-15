from fastapi import APIRouter, HTTPException, Request

from backend.agent.groq_client import run_agent
from backend.api.middleware.rate_limit import limiter
from backend.schemas.request import AskRequest
from backend.schemas.response import AskResponse

router = APIRouter()

# In-memory session store — replaced by Redis in Step 15
_sessions: dict[str, list[dict]] = {}


@router.post("/ask", response_model=AskResponse)
@limiter.limit("30/minute")
async def ask(request: Request, body: AskRequest):
    """
    Main chat endpoint. Sends a message to AEGIS and returns its reply.
    Maintains conversation history per session_id.
    """
    session_id = body.session_id

    # Load existing history for this session (or start fresh)
    history = _sessions.get(session_id, [])

    # Run the Groq tool-use loop
    reply, tools_used = run_agent(history, body.message)

    # Append the new user message + assistant reply to history
    history.append({"role": "user", "content": body.message})
    history.append({"role": "assistant", "content": reply})

    # Save updated history back to session store
    _sessions[session_id] = history

    return AskResponse(
        session_id=session_id,
        reply=reply,
        tools_used=tools_used,
    )


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    del _sessions[session_id]
    return {"message": f"Session {session_id} cleared successfully"}