"""Logging utilities for the AutoDev platform"""

import logging
import logging.handlers
import os
from typing import Optional

def get_logger(name: str, log_level: str = 'INFO') -> logging.Logger:
    """Get or create a logger instance"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Console handler
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def setup_logging(
    log_file: Optional[str] = None,
    log_level: str = 'INFO',
    log_dir: str = 'logs'
) -> None:
    """Setup logging configuration for the entire application"""
    
    # Create logs directory if it doesn't exist
    if log_file and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = os.path.join(log_dir, log_file)
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
