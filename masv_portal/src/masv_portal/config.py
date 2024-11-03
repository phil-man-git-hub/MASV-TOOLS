#!/usr/bin/env python3

# python/masv_portal/src/masv_portal/config.py

"""
Useful utilities for other modules.

This module provides common functionality used throughout the MASV portal client,
including environment variable handling, debugging, and error management.
"""

import os
import sys
from typing import NoReturn, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

TOOL_NAME = 'masv_portal'

def die(cause: str) -> NoReturn:
    """
    Print an error message and exit with status code 1.
    
    Args:
        cause: The error message to display
    """
    debug(cause)
    sys.exit(1)

def debug(msg: str) -> None:
    """
    Print a debug message to stderr with the tool name prefix.
    
    Args:
        msg: The message to display
    """
    print(f"{TOOL_NAME}: {msg}", file=sys.stderr)

def get_api_key() -> str:
    """
    Get the MASV API key from environment variables.
    
    Returns:
        The API key string
        
    Raises:
        SystemExit: If MASV_API_KEY environment variable is not set
    """
    api_key = os.environ.get('MASV_API_KEY')
    if not api_key:
        die("MASV_API_KEY environment variable not set")
    return api_key

def get_team() -> str:
    """
    Get the MASV team ID from environment variables.
    
    Returns:
        The team ID string
        
    Raises:
        SystemExit: If MASV_TEAM environment variable is not set
    """
    team = os.environ.get('MASV_TEAM')
    if not team:
        die("MASV_TEAM environment variable not set")
    return team