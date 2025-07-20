"""Logging configuration and utilities."""

import logging
from pathlib import Path
from ..config import config


def setup_logging() -> logging.Logger:
    """Set up application logging with file and console handlers."""

    # Create a logs directory if it doesn't exist
    log_path = Path(config.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Clear any existing handlers
    logging.getLogger().handlers.clear()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

    # Get logger for this module
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Level: {config.LOG_LEVEL}")

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(name)
