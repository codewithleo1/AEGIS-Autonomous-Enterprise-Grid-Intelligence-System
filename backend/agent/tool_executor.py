from backend.logger import log_tool_call, setup_logger
from backend.services import employee_service, report_service, ticket_service

logger = setup_logger(__name__)

TOOL_MAP = {
    "create_ticket":      ("ticket_service",   "create_ticket_async"),
    "get_ticket_status":  ("ticket_service",   "get_ticket_status_async"),
    "list_tickets":       ("ticket_service",   "list_tickets_async"),
    "update_ticket":      ("ticket_service",   "update_ticket_async"),
    "get_employee_info":  ("employee_service", "get_employee_info_async"),
    "generate_report":    ("report_service",   "generate_report_async"),
}

_SERVICE_MODULES = {
    "ticket_service":   ticket_service,
    "employee_service": employee_service,
    "report_service":   report_service,
}


async def execute_tool(tool_name: str, tool_args: dict) -> dict:
    entry = TOOL_MAP.get(tool_name)

    if entry is None:
        return {"error": f"Unknown tool: {tool_name}"}

    module_name, fn_name = entry
    tool_fn = getattr(_SERVICE_MODULES[module_name], fn_name)

    try:
        result = await tool_fn(**tool_args)
        log_tool_call(logger, tool_name, tool_args, result)
        return result
    except Exception as e:
        logger.error("Tool %s failed: %s", tool_name, str(e))
        return {"error": f"Tool execution failed: {str(e)}"}