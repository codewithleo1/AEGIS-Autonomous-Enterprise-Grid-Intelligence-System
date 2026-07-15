import json

from groq import Groq

from backend.agent.tools import TOOLS
from backend.config import settings
from backend.schemas.response import ToolCall

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


async def run_agent(history: list[dict], new_message: str) -> tuple[str, list[ToolCall]]:
    """
    Run the Groq tool-use loop for one user turn.
    Now fully async — no threading needed.
    """
    from backend.agent.tool_executor import execute_tool

    client = Groq(api_key=settings.groq_api_key)
    tools_used: list[ToolCall] = []

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": new_message},
    ]

    max_retries = 2
    attempt = 0

    while True:
        try:
            response = client.chat.completions.create(
                model=settings.groq_model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
            )
        except Exception as e:
            attempt += 1
            if attempt <= max_retries:
                response = client.chat.completions.create(
                    model=settings.groq_model,
                    messages=messages,
                )
                reply = response.choices[0].message.content
                break
            raise e

        choice = response.choices[0]

        if choice.finish_reason == "stop":
            reply = choice.message.content
            break

        if choice.finish_reason == "tool_calls":
            messages.append(choice.message)

            for tool_call in choice.message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                tool_result = await execute_tool(tool_name, tool_args)

                tools_used.append(
                    ToolCall(
                        tool_name=tool_name,
                        args=tool_args,
                        result=tool_result,
                    )
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result),
                    }
                )

            continue

    return reply, tools_used
