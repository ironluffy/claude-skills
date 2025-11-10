"""
Constants Base - Common configuration values for all Claude Skills
====================================================================

Provides centralized configuration that can be shared across multiple skills.
Skills can import these and extend with skill-specific constants.
"""

from pathlib import Path

# =============================================================================
# GENERAL SETTINGS
# =============================================================================

# Default timeout for operations (milliseconds)
DEFAULT_TIMEOUT = 30000  # 30 seconds

# Default retry attempts
DEFAULT_MAX_RETRIES = 3

# Delay between retries (milliseconds)
DEFAULT_RETRY_DELAY = 1000  # 1 second


# =============================================================================
# FILE PATHS
# =============================================================================

# Default output directory
DEFAULT_OUTPUT_DIR = Path('output')

# Default report directory
DEFAULT_REPORT_DIR = Path('reports')

# Default log directory
DEFAULT_LOG_DIR = Path('logs')

# Default cache directory
DEFAULT_CACHE_DIR = Path('.cache')


# =============================================================================
# OUTPUT FORMATS
# =============================================================================

# Supported output formats
SUPPORTED_OUTPUT_FORMATS = ['json', 'html', 'markdown', 'text']

# Default output format
DEFAULT_OUTPUT_FORMAT = 'html'


# =============================================================================
# CONSOLE OUTPUT
# =============================================================================

# Console message prefixes (for non-logger output)
MSG_INFO = '[*]'
MSG_SUCCESS = '[✓]'
MSG_ERROR = '[✗]'
MSG_WARNING = '[!]'

# Default section divider width
DEFAULT_SECTION_WIDTH = 60

# Progress bar width
PROGRESS_BAR_WIDTH = 50


# =============================================================================
# API SETTINGS
# =============================================================================

# Default API timeout (seconds)
DEFAULT_API_TIMEOUT = 30

# Default rate limit (requests per second)
DEFAULT_RATE_LIMIT = 10

# Default max concurrent requests
DEFAULT_MAX_CONCURRENT = 5


# =============================================================================
# REPORT SETTINGS
# =============================================================================

# Report generator metadata
REPORT_GENERATOR_NAME = 'Claude Skills'

# Include timestamp in reports
REPORT_INCLUDE_TIMESTAMP = True

# Include generator info in reports
REPORT_INCLUDE_GENERATOR = True


# =============================================================================
# ERROR HANDLING
# =============================================================================

# Whether to show full stack traces
SHOW_STACK_TRACES = False

# Whether to continue on errors
CONTINUE_ON_ERROR = False


# =============================================================================
# VALIDATION
# =============================================================================

# Maximum file size for processing (bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Allowed file extensions (can be extended per skill)
ALLOWED_EXTENSIONS = ['.txt', '.md', '.json', '.yaml', '.yml']

# Maximum string length for inputs
MAX_STRING_LENGTH = 10000


# =============================================================================
# PERFORMANCE
# =============================================================================

# Enable caching
ENABLE_CACHE = True

# Cache expiration (seconds)
CACHE_EXPIRATION = 3600  # 1 hour

# Enable parallel processing
ENABLE_PARALLEL = True

# Default worker pool size
DEFAULT_WORKER_POOL_SIZE = 4
