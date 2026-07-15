import json
import logging
import sys


def setup_logger(name: str = "aegis") -> logging.Logger:
    """
    Create and configure a logger with console output.
    Call this once per module: logger = setup_logger(__name__)
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Console handler — prints to stdout (visible in terminal + Fly.io logs)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def log_tool_call(logger: logging.Logger, tool_name: str, args: dict, result: dict) -> None:
    """
    Log a tool call with its arguments and result.
    Call this from tool_executor.py after every tool execution.
    """
    logger.info(
        "TOOL CALL: %s | args: %s | result: %s",
        tool_name,
        json.dumps(args),
        json.dumps(result),
    )