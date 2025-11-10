"""
Logger - Standardized console output for all Claude Skills
===========================================================

Provides consistent, colored console output across all skills.
All scripts should use this instead of direct print() calls.
"""

import sys
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    """Log level enumeration"""
    DEBUG = 0
    INFO = 1
    SUCCESS = 2
    WARNING = 3
    ERROR = 4


class Logger:
    """Standardized logger for console output

    Provides consistent formatting with colored output and icons.
    All skills should use this for console output.

    Example:
        ```python
        from shared.logger import Logger

        logger = Logger()
        logger.info("Starting process...")
        logger.success("Operation completed!")
        logger.error("Something went wrong!")
        ```
    """

    # ANSI color codes
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'gray': '\033[90m',
    }

    def __init__(self, use_colors: bool = True, min_level: LogLevel = LogLevel.DEBUG):
        """Initialize logger

        Args:
            use_colors: Enable colored output (default: True)
            min_level: Minimum log level to display (default: DEBUG)
        """
        self.use_colors = use_colors and sys.stdout.isatty()
        self.min_level = min_level

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled"""
        if not self.use_colors:
            return text
        return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"

    def _format_message(self, prefix: str, message: str, color: str) -> str:
        """Format a log message with prefix and color"""
        colored_prefix = self._colorize(prefix, color)
        return f"{colored_prefix} {message}"

    def debug(self, message: str) -> None:
        """Log debug message (gray, lowest priority)"""
        if self.min_level.value <= LogLevel.DEBUG.value:
            formatted = self._format_message('[DEBUG]', message, 'gray')
            print(formatted)

    def info(self, message: str) -> None:
        """Log info message (blue [*])"""
        if self.min_level.value <= LogLevel.INFO.value:
            formatted = self._format_message('[*]', message, 'blue')
            print(formatted)

    def success(self, message: str) -> None:
        """Log success message (green [✓])"""
        if self.min_level.value <= LogLevel.SUCCESS.value:
            formatted = self._format_message('[✓]', message, 'green')
            print(formatted)

    def warning(self, message: str) -> None:
        """Log warning message (yellow [!])"""
        if self.min_level.value <= LogLevel.WARNING.value:
            formatted = self._format_message('[!]', message, 'yellow')
            print(formatted)

    def error(self, message: str, file=None) -> None:
        """Log error message (red [✗])"""
        if self.min_level.value <= LogLevel.ERROR.value:
            formatted = self._format_message('[✗]', message, 'red')
            print(formatted, file=file or sys.stderr)

    def section(self, title: str, char: str = '=', width: int = 60) -> None:
        """Print a section divider with title

        Args:
            title: Section title
            char: Character to use for divider (default: '=')
            width: Total width of divider (default: 60)
        """
        print()
        print(char * width)
        print(title)
        print(char * width)

    def table_row(
        self,
        columns: list[str],
        widths: Optional[list[int]] = None,
        separator: str = ' | '
    ) -> None:
        """Print a formatted table row

        Args:
            columns: List of column values
            widths: Optional list of column widths (auto-calculated if None)
            separator: Column separator (default: ' | ')
        """
        if widths is None:
            widths = [len(col) for col in columns]

        formatted_cols = [
            col.ljust(width) for col, width in zip(columns, widths)
        ]
        print(separator.join(formatted_cols))

    def progress(
        self,
        current: int,
        total: int,
        prefix: str = '',
        suffix: str = '',
        length: int = 50
    ) -> None:
        """Print a progress bar

        Args:
            current: Current progress value
            total: Total/maximum value
            prefix: Text before progress bar
            suffix: Text after progress bar
            length: Length of progress bar in characters
        """
        if total == 0:
            percent = 100
        else:
            percent = int(100 * current / total)

        filled = int(length * current / total) if total > 0 else length
        bar = '█' * filled + '░' * (length - filled)

        # Use carriage return to overwrite same line
        output = f'\r{prefix} |{bar}| {percent}% {suffix}'
        print(output, end='', flush=True)

        # Print newline when complete
        if current >= total:
            print()


# Global logger instance for convenience
default_logger = Logger()


# Convenience functions that use the default logger
def debug(message: str) -> None:
    """Log debug message using default logger"""
    default_logger.debug(message)


def info(message: str) -> None:
    """Log info message using default logger"""
    default_logger.info(message)


def success(message: str) -> None:
    """Log success message using default logger"""
    default_logger.success(message)


def warning(message: str) -> None:
    """Log warning message using default logger"""
    default_logger.warning(message)


def error(message: str) -> None:
    """Log error message using default logger"""
    default_logger.error(message)


def section(title: str, char: str = '=', width: int = 60) -> None:
    """Print section divider using default logger"""
    default_logger.section(title, char, width)
