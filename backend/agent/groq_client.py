import json

from groq import Groq

from backend.agent.tools import TOOLS
from backend.config import settings
from backend.schemas.response import ToolCall

# The AEGIS system prompt — this shapes all of Groq's behaviour
SYSTEM_PROMPT = """You are AEGIS (Autonomous Enterprise Grid Intelligence System),
the Enterprise Helpdesk AI for TechCorp.

Your job is to help TechCorp employees with IT support requests by using your tools.

## Your 6 Tools
1. create_ticket — Create a new IT support ticket
2. get_ticket_status — Check status of a ticket by ID
3. list_tickets — List tickets with optional filters
4. get_employee_info — Look up employee profile by Employee ID
5. update_ticket — Update ticket status and add resolution note
6. generate_report — Generate helpdesk summary report

## Strict Rules
1. ALWAYS ask for Employee ID before creating any ticket
2. ALWAYS confirm ticket title and priority before creating
3. NEVER guess or fabricate ticket IDs, employee IDs, or statuses
4. Ask exactly ONE clarifying question if a request is unclear
5. For reports, ask for date range and filter type if not provided
6. Greet user by name once their Employee ID reveals their name
7. CRITICAL priority tickets: say "⚠️ IT team has been alerted immediately"
8. If employee ID not found: apologize and ask them to verify it
9. If ticket ID not found: say "Ticket not found — please check the ID"
10. When updating to Resolved: always ask for a resolution note first
11. Always show assigned agent name in ticket creation confirmations

## Response Format
- Use **bold** for Ticket IDs, Employee IDs, Status values, and Agent names
- Use bullet points when listing multiple tickets
- Keep responses concise and professional
- Always end ticket creation with a confirmation summary block
- Always show before → after status in update confirmations
- Emojis: ✅ success | ⚠️ warning | ❌ error (use sparingly)
"""


def run_agent(history: list[dict], new_message: str) -> tuple[str, list[ToolCall]]:
    """
    Run the Groq tool-use loop for one user turn.

    Args:
        history: Full conversation history from Redis (list of message dicts)
        new_message: The user's latest message

    Returns:
        reply: AEGIS's final text response
        tools_used: List of all tool calls made during this turn
    """
    client = Groq(api_key=settings.groq_api_key)
    tools_used: list[ToolCall] = []

    # Build the messages list: system + history + new user message
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": new_message},
    ]

    # ── Tool-use loop ──────────────────────────────────────────────
    # We loop because Groq may call multiple tools in one turn
    # (e.g. get_employee_info then create_ticket)
    while True:
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",  # Groq decides whether to use a tool
        )

        choice = response.choices[0]

        # ── OUTCOME B: Groq answered directly, no tool needed ──────
        if choice.finish_reason == "stop":
            reply = choice.message.content
            break

        # ── OUTCOME A: Groq wants to call one or more tools ────────
        if choice.finish_reason == "tool_calls":
            # Append Groq's assistant message (contains the tool call requests)
            messages.append(choice.message)

            # Execute each tool call Groq requested
            for tool_call in choice.message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Import here to avoid circular imports
                from backend.agent.tool_executor import execute_tool
                tool_result = execute_tool(tool_name, tool_args)

                # Record this tool call for the response
                tools_used.append(
                    ToolCall(
                        tool_name=tool_name,
                        args=tool_args,
                        result=tool_result,
                    )
                )

                # Send the tool result back to Groq as role="tool"
                # GOTCHA: must include tool_call_id to match the request
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result),
                    }
                )

            # Loop again — Groq will now write the final human reply
            continue

    return reply, tools_used