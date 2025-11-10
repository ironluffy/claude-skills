"""
CLI Utils - Common command-line interface utilities
====================================================

Provides reusable CLI components for argparse and command-line handling
across all Claude Skills.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List, Callable
from functools import wraps

from .logger import Logger
from .constants_base import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_OUTPUT_FORMAT,
    SUPPORTED_OUTPUT_FORMATS
)


def create_base_parser(description: str, epilog: Optional[str] = None) -> argparse.ArgumentParser:
    """Create a base argument parser with common options

    Args:
        description: Description of the script
        epilog: Optional epilog text with examples

    Returns:
        ArgumentParser with common arguments pre-configured
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )

    return parser


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to a parser

    Args:
        parser: ArgumentParser to add arguments to
    """
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress non-error output'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )


def add_output_arguments(parser: argparse.ArgumentParser, required: bool = False) -> None:
    """Add output-related arguments to a parser

    Args:
        parser: ArgumentParser to add arguments to
        required: Whether output path is required
    """
    parser.add_argument(
        '--output', '-o',
        type=Path,
        required=required,
        help='Output file path' + (' (required)' if required else '')
    )

    parser.add_argument(
        '--format', '-f',
        choices=SUPPORTED_OUTPUT_FORMATS,
        default=DEFAULT_OUTPUT_FORMAT,
        help=f'Output format (default: {DEFAULT_OUTPUT_FORMAT})'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f'Output directory (default: {DEFAULT_OUTPUT_DIR})'
    )


def add_url_argument(parser: argparse.ArgumentParser, required: bool = True) -> None:
    """Add URL argument to a parser

    Args:
        parser: ArgumentParser to add argument to
        required: Whether URL is required
    """
    parser.add_argument(
        '--url',
        required=required,
        help='URL to analyze/test' + (' (required)' if required else '')
    )


def add_file_argument(parser: argparse.ArgumentParser, required: bool = True) -> None:
    """Add file input argument to a parser

    Args:
        parser: ArgumentParser to add argument to
        required: Whether file is required
    """
    parser.add_argument(
        '--file',
        type=Path,
        required=required,
        help='Input file path' + (' (required)' if required else '')
    )


def validate_file_exists(file_path: Path) -> bool:
    """Validate that a file exists

    Args:
        file_path: Path to validate

    Returns:
        bool: True if file exists, False otherwise
    """
    if not file_path.exists():
        return False
    if not file_path.is_file():
        return False
    return True


def validate_url(url: str) -> bool:
    """Basic URL validation

    Args:
        url: URL to validate

    Returns:
        bool: True if URL appears valid, False otherwise
    """
    if not url:
        return False

    # Basic check for http/https
    if not (url.startswith('http://') or url.startswith('https://')):
        return False

    return True


def handle_cli_errors(func: Callable) -> Callable:
    """Decorator for handling CLI errors gracefully

    Example:
        ```python
        @handle_cli_errors
        def main():
            # Your main logic
            pass
        ```
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = Logger()

        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            logger.warning("\nOperation cancelled by user")
            sys.exit(130)  # Standard exit code for SIGINT
        except Exception as e:
            logger.error(f"Error: {e}")
            if '--verbose' in sys.argv or '-v' in sys.argv:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    return wrapper


def confirm_action(prompt: str, default: bool = False) -> bool:
    """Prompt user for confirmation

    Args:
        prompt: Prompt message to display
        default: Default value if user just presses Enter

    Returns:
        bool: True if user confirmed, False otherwise
    """
    default_str = 'Y/n' if default else 'y/N'
    response = input(f"{prompt} [{default_str}]: ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']


def print_summary_table(headers: List[str], rows: List[List[str]], widths: Optional[List[int]] = None) -> None:
    """Print a formatted table to console

    Args:
        headers: List of header labels
        rows: List of rows (each row is a list of values)
        widths: Optional list of column widths
    """
    if widths is None:
        # Auto-calculate widths
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))

    # Print header
    header_row = ' | '.join(h.ljust(w) for h, w in zip(headers, widths))
    print(header_row)
    print('-' * len(header_row))

    # Print rows
    for row in rows:
        print(' | '.join(str(cell).ljust(w) for cell, w in zip(row, widths)))


# Example usage
if __name__ == '__main__':
    # Example: Create a parser with common arguments
    parser = create_base_parser(
        description='Example CLI tool',
        epilog='''
Examples:
  python script.py --url https://example.com --output report.html
  python script.py --file input.json --format json --verbose
        '''
    )

    add_common_arguments(parser)
    add_output_arguments(parser, required=True)
    add_url_argument(parser)

    args = parser.parse_args()

    # Create logger based on arguments
    logger = Logger(
        use_colors=not args.no_color
    )

    logger.info("Example CLI utility")
    logger.success("Arguments parsed successfully!")

    # Example table
    print_summary_table(
        headers=['Name', 'Status', 'Time'],
        rows=[
            ['Test 1', 'PASS', '1.2s'],
            ['Test 2', 'PASS', '2.3s'],
            ['Test 3', 'FAIL', '0.5s'],
        ]
    )
