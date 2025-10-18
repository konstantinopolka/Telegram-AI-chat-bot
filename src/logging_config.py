"""
Centralized logging configuration for the entire project.

Usage:
    from src.logging_config import setup_logging, get_logger
    
    # In main.py
    setup_logging()
    
    # In any module
    logger = get_logger(__name__)
    logger.info("Hello world")
"""

import logging
import logging.handlers
import sys
import os
from pathlib import Path
from typing import Optional

def setup_logging(
    level: str = "INFO",
    log_file: str = "bot.log",
    log_to_console: bool = True,
    log_to_file: bool = True,
    json_format: bool = False,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> None:
    """
    Configure logging for the entire application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        log_to_console: Whether to log to console
        log_to_file: Whether to log to file
        json_format: Whether to use JSON formatting (useful for log aggregators)
        max_file_size: Maximum size of log file before rotation (bytes)
        backup_count: Number of backup log files to keep
    
    Example:
        # In main.py
        setup_logging(level="DEBUG", log_file="logs/bot.log")
    """
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove any existing handlers (prevents duplicate logs)
    root_logger.handlers.clear()
    
    # Create formatters
    if json_format:
        # JSON format for structured logging
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", '
            '"message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", '
            '"line": %(lineno)d}'
        )
    else:
        # Human-readable format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)  # Console shows all levels
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_to_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Rotating file handler (creates new file when size limit reached)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific log levels for noisy libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    
    # Log that logging is configured
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured: level={level}, file={log_file}")
    

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Logger instance
    
    Example:
        logger = get_logger(__name__)
        logger.info("Starting process")
    """
    return logging.getLogger(name)

def set_module_level(module_name: str, level: str) -> None:
    """
    Set log level for a specific module.
    
    Args:
        module_name: Module name (e.g., "src.dao.repositories")
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Example:
        # Make database module verbose
        set_module_level("src.dao", "DEBUG")
        
        # Silence scraping module
        set_module_level("src.scraping", "WARNING")
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(getattr(logging, level.upper()))
    logging.getLogger(__name__).info(
        f"Set log level for '{module_name}' to {level.upper()}"
    )