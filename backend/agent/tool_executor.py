from backend.logger import log_tool_call, setup_logger
from backend.services.employee_service import get_employee_info
from backend.services.report_service import generate_report
from backend.services.ticket_service import create_ticket, get_ticket_status, list_tickets, update_ticket

logger = setup_logger(__name__)

TOOL_MAP = {
    "create_ticket": create_ticket,
    "get_ticket_status": get_ticket_status,
    "list_tickets": list_tickets,
    "get_employee_info": get_employee_info,
    "update_ticket": update_ticket,
    "generate_report": generate_report,
}


def execute_tool(tool_name: str, tool_args: dict) -> dict:
    """
    Dispatch a tool call from Groq to the correct service function.
    Logs every tool call for observability.
    """
    tool_fn = TOOL_MAP.get(tool_name)

    if tool_fn is None:
        return {"error": f"Unknown tool: {tool_name}"}

    try:
        result = tool_fn(**tool_args)
        log_tool_call(logger, tool_name, tool_args, result)
        return result
    except Exception as e:
        logger.error("Tool %s failed: %s", tool_name, str(e))
        return {"error": f"Tool execution failed: {str(e)}"}