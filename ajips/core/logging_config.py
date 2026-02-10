"""
Logging configuration for AJIPS application.
Provides structured logging with JSON output for production environments.
"""

import logging
import sys
from logging import Logger

from pythonjsonlogger import jsonlogger


def setup_logging(app_name: str = "ajips", level: str = "INFO") -> Logger:
    """
    Configure structured JSON logging for the application.

    Args:
        app_name: Application name for log identification
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(app_name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # JSON formatter for structured logging
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(timestamp)s %(level)s %(name)s %(message)s",
        timestamp=True,
    )

    # Console handler with JSON output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> Logger:
    """Get or create a logger with the given name."""
    return logging.getLogger(name)
