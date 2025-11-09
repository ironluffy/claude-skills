"""
Constants - Centralized configuration values
Part of web-app-qa skill for Claude Skills

All magic numbers, timeouts, and configuration values in one place.
"""

# =============================================================================
# TIMEOUTS (milliseconds)
# =============================================================================

# Default navigation timeout for page.goto()
DEFAULT_NAVIGATION_TIMEOUT = 30000  # 30 seconds

# Default load state timeout
DEFAULT_LOAD_TIMEOUT = 10000  # 10 seconds

# Timeout for waiting for network idle
NETWORK_IDLE_TIMEOUT = 10000  # 10 seconds

# DOM stability check timeout
DOM_STABLE_TIMEOUT = 10000  # 10 seconds

# DOM stability check interval
DOM_STABLE_CHECK_INTERVAL = 100  # 100ms


# =============================================================================
# VIEWPORTS - Standard device sizes
# =============================================================================

VIEWPORTS = {
    # Desktop
    'desktop': {
        'width': 1920,
        'height': 1080
    },

    # Laptop
    'laptop': {
        'width': 1366,
        'height': 768
    },

    # Tablet (iPad)
    'tablet': {
        'width': 768,
        'height': 1024
    },

    # Mobile (iPhone)
    'mobile': {
        'width': 375,
        'height': 667
    },

    # Mobile landscape
    'mobile_landscape': {
        'width': 667,
        'height': 375
    },

    # Large desktop
    'desktop_4k': {
        'width': 3840,
        'height': 2160
    }
}


# =============================================================================
# VISUAL REGRESSION SETTINGS
# =============================================================================

# Default difference threshold (0-1, where 0.05 = 5%)
DEFAULT_DIFF_THRESHOLD = 0.05

# Diff enhancement factor for visualization
DIFF_ENHANCEMENT_FACTOR = 10

# Font path for visual diff labels (macOS)
MACOS_FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

# Default font size for diff labels
DIFF_LABEL_FONT_SIZE = 20

# Label height in diff images
DIFF_LABEL_HEIGHT = 40


# =============================================================================
# ACCESSIBILITY SETTINGS
# =============================================================================

# WCAG compliance levels and their corresponding axe-core tags
WCAG_LEVELS = {
    'WCAG-A': ['wcag2a', 'wcag21a'],
    'WCAG-AA': ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'],
    'WCAG-AAA': ['wcag2a', 'wcag2aa', 'wcag2aaa', 'wcag21a', 'wcag21aa', 'wcag21aaa']
}

# Default WCAG standard
DEFAULT_WCAG_STANDARD = 'WCAG-AA'


# =============================================================================
# BROWSER SETTINGS
# =============================================================================

# Supported browser types
SUPPORTED_BROWSERS = ['chromium', 'firefox', 'webkit']

# Browser aliases
BROWSER_ALIASES = {
    'chrome': 'chromium',
    'ff': 'firefox',
    'safari': 'webkit'
}

# Default headless mode
DEFAULT_HEADLESS = True


# =============================================================================
# REPORT SETTINGS
# =============================================================================

# Report generator metadata
REPORT_GENERATOR_NAME = 'web-app-qa skill'

# Default report format
DEFAULT_REPORT_FORMAT = 'html'

# Screenshot quality (for JPEG/WebP)
SCREENSHOT_QUALITY = 90


# =============================================================================
# RETRY SETTINGS
# =============================================================================

# Maximum retry attempts for navigation
MAX_NAVIGATION_RETRIES = 3

# Maximum retry attempts for element interactions
MAX_INTERACTION_RETRIES = 3

# Delay between retries (milliseconds)
RETRY_DELAY = 1000


# =============================================================================
# FILE PATHS
# =============================================================================

# Default output directory names
DEFAULT_BASELINE_DIR = 'baselines'
DEFAULT_DIFF_DIR = 'diffs'
DEFAULT_REPORT_DIR = 'reports'
DEFAULT_SCREENSHOT_DIR = 'screenshots'
DEFAULT_TEST_DIR = 'tests'


# =============================================================================
# CONSOLE OUTPUT
# =============================================================================

# Console message prefixes
MSG_INFO = '[*]'
MSG_SUCCESS = '[✓]'
MSG_ERROR = '[✗]'
MSG_WARNING = '[!]'

# Progress indicators
PROGRESS_BAR_WIDTH = 60
