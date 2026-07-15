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
    """
    Main chat endpoint. Sends a message to AEGIS and returns its reply.
    Conversation history is persisted in Upstash Redis per session_id.
    """
    session_id = body.session_id

    # Load existing history from Redis (empty list if new session)
    history = load_session(session_id)

    # Run the Groq tool-use loop
    reply, tools_used = run_agent(history, body.message)

    # Append new user message + assistant reply to history
    history.append({"role": "user", "content": body.message})
    history.append({"role": "assistant", "content": reply})

    # Save updated history back to Redis
    save_session(session_id, history)

    return AskResponse(
        session_id=session_id,
        reply=reply,
        tools_used=tools_used,
    )


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session from Redis."""
    deleted = delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": f"Session {session_id} cleared successfully"}
