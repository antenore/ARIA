"""
Logging configuration for ARIA.

This module sets up logging for the ARIA framework.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional, Union, Literal

from rich.logging import RichHandler

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def setup_logger(
    name: str = "aria",
    level: Union[LogLevel, str] = "INFO",
    log_file: Optional[Union[str, Path]] = None,
) -> logging.Logger:
    """Set up and configure logger.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional path to log file
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level.upper())
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatters
    console_formatter = logging.Formatter(
        "%(message)s",
        datefmt="[%X]"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Console handler (using Rich)
    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_path=False,
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log file specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(str(log_path), encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create default logger
logger: logging.Logger = setup_logger()

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get logger instance.
    
    Args:
        name: Optional logger name
        
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"aria.{name}")
    return logger