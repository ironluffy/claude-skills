"""
Constants - Centralized configuration values
Part of system-design-reviewer skill for Claude Skills

All magic values, file patterns, and configuration in one place.
"""

# =============================================================================
# FILE PATTERNS
# =============================================================================

# Code file extensions to analyze
CODE_EXTENSIONS = ['.py', '.js', '.java', '.rb', '.php', '.go', '.ts', '.jsx', '.tsx', '.rs']

# Configuration file extensions
CONFIG_EXTENSIONS = ['.yml', '.yaml', '.json', '.conf', '.ini', '.toml', '.env']

# Documentation file extensions
DOC_EXTENSIONS = ['.md', '.txt', '.rst', '.adoc']

# Files to skip during analysis
SKIP_PATTERNS = [
    'node_modules',
    '.git',
    '__pycache__',
    'venv',
    'env',
    '.env',
    'dist',
    'build',
    'target',
    '.next',
    'coverage'
]


# =============================================================================
# SECURITY PATTERNS
# =============================================================================

# Secret detection patterns
SECRET_PATTERNS = {
    "api_key": r'(?i)(api[_-]?key|apikey)\s*=\s*[\'"]([a-zA-Z0-9]{20,})[\'"]',
    "password": r'(?i)(password|passwd|pwd)\s*=\s*[\'"](?!{{)[^\'"]{8,}[\'"]',
    "token": r'(?i)(token|auth[_-]?token)\s*=\s*[\'"]([a-zA-Z0-9]{20,})[\'"]',
    "secret": r'(?i)(secret|secret[_-]?key)\s*=\s*[\'"]([a-zA-Z0-9]{20,})[\'"]',
    "private_key": r'(?i)(private[_-]?key|privatekey)\s*=\s*[\'"]([a-zA-Z0-9]{20,})[\'"]'
}

# Security technology indicators
SECURITY_INDICATORS = {
    'https': ['https://', 'ssl', 'tls'],
    'password_hashing': ['bcrypt', 'argon2', 'scrypt', 'pbkdf2'],
    'rate_limiting': ['rate-limit', 'ratelimit', 'throttle'],
    'csrf': ['csrf', 'csrf-token', 'xsrf'],
    'security_headers': ['csp', 'x-frame-options', 'hsts', 'x-content-type-options'],
    'input_validation': ['validator', 'sanitize', 'validate', 'joi', 'yup']
}


# =============================================================================
# ARCHITECTURE PATTERNS
# =============================================================================

# Architecture component indicators
ARCHITECTURE_INDICATORS = {
    'database_replication': ['replica', 'replication', 'read_replica', 'slave', 'standby'],
    'caching': ['redis', 'memcache', 'cache'],
    'load_balancer': ['nginx.conf', 'haproxy.cfg', 'load-balancer', 'alb', 'elb'],
    'health_checks': ['/health', '/ready', '/ping', '/status', 'healthcheck'],
    'monitoring': ['prometheus', 'grafana', 'datadog', 'newrelic', 'sentry'],
    'logging': ['winston', 'log4j', 'logback', 'logging', 'logger']
}

# Directory structure indicators
MVC_DIRECTORIES = ['controllers', 'models', 'views', 'services']
LAYERED_DIRECTORIES = ['domain', 'application', 'infrastructure', 'presentation']


# =============================================================================
# PERFORMANCE PATTERNS
# =============================================================================

# Performance technology indicators
PERFORMANCE_INDICATORS = {
    'caching': ['redis', 'memcache', 'cache'],
    'connection_pooling': ['connection.pool', 'pool.size', 'max.connections', 'pooling'],
    'async_processing': ['async', 'await', 'celery', 'sidekiq', 'bull', 'queue'],
    'database_indexes': ['index', 'create index', 'add_index'],
    'cdn': ['cloudfront', 'cloudflare', 'cdn', 'content delivery'],
    'compression': ['gzip', 'compress', 'compression']
}

# N+1 query indicators
N_PLUS_ONE_PATTERNS = [
    r'for\s+\w+\s+in\s+.*:\s*\w+\.query',  # Python
    r'\.forEach\(.*=>\s*.*\.find',  # JavaScript
    r'\.each\s+do.*\w+\.find',  # Ruby
]


# =============================================================================
# COST OPTIMIZATION
# =============================================================================

# Cloud service cost indicators
CLOUD_SERVICE_PATTERNS = {
    'aws': ['ec2', 'rds', 's3', 'lambda', 'dynamodb'],
    'gcp': ['compute engine', 'cloud sql', 'cloud storage'],
    'azure': ['virtual machines', 'sql database', 'blob storage']
}

# Right-sizing recommendations
INSTANCE_SIZES = ['nano', 'micro', 'small', 'medium', 'large', 'xlarge', '2xlarge']


# =============================================================================
# ANALYSIS THRESHOLDS
# =============================================================================

# Severity thresholds
SEVERITY_THRESHOLDS = {
    'critical': {'security': 1, 'performance': 0},
    'high': {'architecture': 2, 'security': 1, 'performance': 2},
    'medium': {'architecture': 5, 'security': 3, 'performance': 5},
    'low': {'architecture': 10, 'security': 5, 'performance': 10}
}

# Effort estimates (hours)
EFFORT_ESTIMATES = {
    'trivial': '1 hour',
    'easy': '2-4 hours',
    'medium': '4-8 hours',
    'hard': '1-2 days',
    'complex': '2-5 days'
}

# Cost impact estimates (USD/month)
COST_IMPACTS = {
    'none': 'None',
    'low': '+$10-30/month',
    'medium': '+$30-100/month',
    'high': '+$100-500/month',
    'very_high': '+$500+/month'
}


# =============================================================================
# REPORT SETTINGS
# =============================================================================

# Report sections
REPORT_SECTIONS = [
    'architecture',
    'security',
    'performance',
    'cost',
    'diagrams'
]

# Issue severity colors (for HTML reports)
SEVERITY_COLORS = {
    'critical': '#dc3545',
    'high': '#fd7e14',
    'medium': '#ffc107',
    'low': '#17a2b8',
    'info': '#0d6efd'
}

# Strength indicators
STRENGTH_ICONS = {
    'architecture': '🏗️',
    'security': '🔒',
    'performance': '⚡',
    'cost': '💰',
    'testing': '✅',
    'monitoring': '📊'
}


# =============================================================================
# CONSOLE OUTPUT
# =============================================================================

# Console message prefixes (for backward compatibility)
MSG_INFO = '[*]'
MSG_SUCCESS = '[✓]'
MSG_ERROR = '[✗]'
MSG_WARNING = '[!]'

# Section divider
SECTION_WIDTH = 60


# =============================================================================
# FILE SIZE LIMITS
# =============================================================================

# Maximum file size to analyze (bytes)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Maximum lines to read per file
MAX_LINES_PER_FILE = 10000
