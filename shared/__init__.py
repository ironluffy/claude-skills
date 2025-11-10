"""
Shared Utilities for Claude Skills
====================================

Common utilities and base classes shared across multiple skills.

Modules:
- logger: Standardized console logging
- constants_base: Common configuration values
- report_base: Abstract base for report generators
- cli_utils: Common CLI argument parsing utilities
"""

__version__ = "1.0.0"

from .logger import Logger, LogLevel
from .constants_base import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TIMEOUT,
    SUPPORTED_OUTPUT_FORMATS,
)

__all__ = [
    'Logger',
    'LogLevel',
    'DEFAULT_OUTPUT_DIR',
    'DEFAULT_TIMEOUT',
    'SUPPORTED_OUTPUT_FORMATS',
]
