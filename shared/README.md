# Shared Utilities Library

**Version**: 1.0.0
**Purpose**: Cross-skill utilities for consistent logging, configuration, and report generation across all Claude Skills.

---

## Overview

The `shared/` directory contains reusable utilities that eliminate code duplication and ensure consistency across all skills. These utilities provide:

- ✅ **Professional colored console logging**
- ✅ **Common configuration constants**
- ✅ **Abstract base classes for reports**
- ✅ **CLI argument parsing utilities**

---

## Directory Structure

```
shared/
├── __init__.py              # Package initialization with exports
├── logger.py                # Professional colored logging (235 lines)
├── constants_base.py        # Common configuration values (175 lines)
├── report_base.py           # Abstract report base classes
└── cli_utils.py             # CLI argument parsing utilities
```

---

## Components

### 1. Logger (`logger.py`)

Professional colored console output with ANSI support and log levels.

#### Features

- **5 Log Levels**: DEBUG, INFO, SUCCESS, WARNING, ERROR
- **Colored Output**: ANSI colors with automatic TTY detection
- **Formatted Messages**: Consistent prefixes and timestamps
- **Section Dividers**: Create visual separations in console output
- **Context Manager**: Use with `with` statements for structured logging

#### Usage

```python
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'shared'))
from logger import Logger, LogLevel

# Create logger
logger = Logger(min_level=LogLevel.INFO, use_color=True)

# Basic logging
logger.info("Processing request...")        # Blue [*] prefix
logger.success("Task completed!")           # Green [✓] prefix
logger.warning("Resource running low")      # Yellow [!] prefix
logger.error("Operation failed")            # Red [✗] prefix
logger.debug("Detailed debug info")         # Gray [→] prefix

# Section dividers
logger.section("Architecture Analysis", '=', 80)
# Output: ================================================================================
#         Architecture Analysis
#         ================================================================================

# Context manager for nested sections
with logger.section_context("Analyzing security"):
    logger.info("Scanning for vulnerabilities...")
    logger.success("Found 3 issues")
```

#### API Reference

| Method | Description | Example |
|--------|-------------|---------|
| `info(message)` | Log info message (blue) | `logger.info("Starting...")` |
| `success(message)` | Log success (green) | `logger.success("Done!")` |
| `warning(message)` | Log warning (yellow) | `logger.warning("Check this")` |
| `error(message)` | Log error (red) | `logger.error("Failed")` |
| `debug(message)` | Log debug (gray) | `logger.debug("Details...")` |
| `section(title, char, width)` | Print section divider | `logger.section("Title", '=', 60)` |

#### Log Levels

```python
from logger import LogLevel

# Set minimum log level (filters out lower priority messages)
logger = Logger(min_level=LogLevel.WARNING)  # Only WARNING and ERROR
logger = Logger(min_level=LogLevel.DEBUG)    # All messages

# Log level priority (lowest to highest)
LogLevel.DEBUG < LogLevel.INFO < LogLevel.SUCCESS < LogLevel.WARNING < LogLevel.ERROR
```

#### Color Configuration

```python
# Automatic TTY detection
logger = Logger(use_color=True)  # Colors enabled if TTY

# Force enable/disable colors
logger = Logger(use_color=True)   # Always use colors
logger = Logger(use_color=False)  # Never use colors (for logs)

# Colors automatically disabled when:
# - Output is redirected to file
# - Running in non-TTY environment
# - NO_COLOR environment variable is set
```

---

### 2. Constants Base (`constants_base.py`)

Common configuration values shared across all skills.

#### Key Constants

```python
from constants_base import (
    DEFAULT_TIMEOUT,
    DEFAULT_OUTPUT_DIR,
    MAX_FILE_SIZE,
    SUPPORTED_OUTPUT_FORMATS,
    CODE_EXTENSIONS,
    CONFIG_EXTENSIONS,
    SKIP_DIRECTORIES
)

# File handling
DEFAULT_TIMEOUT = 30000  # 30 seconds (milliseconds)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
LARGE_FILE_THRESHOLD = 1024 * 1024  # 1MB

# Output configuration
DEFAULT_OUTPUT_DIR = Path('output')
SUPPORTED_OUTPUT_FORMATS = ['json', 'html', 'markdown', 'text']

# File extensions
CODE_EXTENSIONS = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.rb', '.go', '.rs']
CONFIG_EXTENSIONS = ['.yml', '.yaml', '.json', '.toml', '.ini', '.conf']
TEST_EXTENSIONS = ['.test.js', '.spec.js', '.test.ts', '.spec.ts', '_test.py']

# Directories to skip during file scanning
SKIP_DIRECTORIES = [
    'node_modules', '.git', '__pycache__', 'venv', '.venv',
    'dist', 'build', '.next', 'coverage', '.pytest_cache'
]
```

#### Adding Skill-Specific Constants

```python
# In your-skill/scripts/constants.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from constants_base import *

# Add skill-specific constants
SKILL_SPECIFIC_PATTERNS = {
    'pattern_group': ['indicator1', 'indicator2'],
}
```

---

### 3. Report Base (`report_base.py`)

Abstract base classes for consistent report generation.

#### Base Classes

```python
from report_base import BaseReportGenerator, HTMLReportBase

class MyReportGenerator(BaseReportGenerator):
    """Custom report generator"""

    def generate(self) -> str:
        """Generate the complete report content"""
        # Your report generation logic
        return report_content

    def save(self, output_path: Path) -> None:
        """Save already implemented in base class"""
        # Automatically creates parent directories
        # Writes content to file
        pass
```

#### HTML Report Base

```python
from report_base import HTMLReportBase

class MyHTMLReport(HTMLReportBase):
    """HTML report with built-in styling"""

    def __init__(self, title: str):
        super().__init__(title)
        self.add_custom_style(".my-class { color: blue; }")

    def generate(self) -> str:
        self.add_section("<h2>My Section</h2>")
        self.add_section("<p>Content here</p>")
        return self.build()
```

**Built-in Styles**: The HTMLReportBase includes professional CSS with:
- Responsive layout (max-width: 1200px)
- Modern font stack (system fonts)
- Color-coded badges (success, warning, error, info)
- Card-based layouts
- Collapsible sections (`<details>`)

---

### 4. CLI Utils (`cli_utils.py`)

Reusable CLI components for consistent command-line interfaces.

#### Usage

```python
from cli_utils import (
    create_base_parser,
    add_common_arguments,
    add_output_arguments,
    handle_cli_errors
)

# Create base parser with description
parser = create_base_parser(
    description="My skill description",
    epilog="Example: python script.py /path/to/project"
)

# Add common arguments (verbose, quiet, debug)
add_common_arguments(parser)

# Add output arguments (--output, --format)
add_output_arguments(parser, required=False)

# Add custom arguments
parser.add_argument('project_path', help='Path to project')

# Parse arguments
args = parser.parse_args()

# Use with error handling decorator
@handle_cli_errors
def main():
    # Your main logic
    pass

if __name__ == "__main__":
    main()
```

#### Common Arguments Added

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--verbose, -v` | flag | False | Enable verbose output |
| `--quiet, -q` | flag | False | Suppress non-error output |
| `--debug` | flag | False | Enable debug output |
| `--output, -o` | str | None | Output file path |
| `--format, -f` | str | 'json' | Output format (json/html/md/txt) |

---

## Integration Guide

### Step 1: Add Import Boilerplate

Add this to the top of your script:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from logger import Logger
from constants_base import CODE_EXTENSIONS, SKIP_DIRECTORIES
```

**Path Breakdown**:
- `Path(__file__)` - Current script location
- `.parent` (1st) - scripts/ directory
- `.parent` (2nd) - skill-name/ directory
- `.parent` (3rd) - claude-skills/ root directory
- `/ 'shared'` - shared/ directory

### Step 2: Replace Print Statements

**Before**:
```python
print("Starting analysis...")
print("✅ Complete!")
print(f"Error: {error_message}")
```

**After**:
```python
logger = Logger()
logger.info("Starting analysis...")
logger.success("Complete!")
logger.error(f"Error: {error_message}")
```

### Step 3: Use Constants

**Before**:
```python
code_files = []
for ext in ['.py', '.js', '.ts', '.jsx', '.tsx']:
    code_files.extend(project_path.rglob(f'*{ext}'))

for file in code_files:
    if 'node_modules' in str(file) or '.git' in str(file):
        continue
```

**After**:
```python
from constants_base import CODE_EXTENSIONS, SKIP_DIRECTORIES

def should_skip(file_path):
    return any(skip_dir in file_path.parts for skip_dir in SKIP_DIRECTORIES)

code_files = []
for ext in CODE_EXTENSIONS:
    for file in project_path.rglob(f'*{ext}'):
        if not should_skip(file):
            code_files.append(file)
```

### Step 4: Generate Reports

```python
from report_base import HTMLReportBase

class MyReport(HTMLReportBase):
    def generate(self):
        self.add_section(f"<h1>{self.title}</h1>")
        # Add content...
        return self.build()

report = MyReport("My Analysis Report")
report.save(Path("output/report.html"))
```

---

## Best Practices

### 1. **Always Use Logger for Output**
```python
# ❌ DON'T
print("Starting...")

# ✅ DO
logger.info("Starting...")
```

### 2. **Import Only What You Need**
```python
# ❌ DON'T
from constants_base import *

# ✅ DO
from constants_base import CODE_EXTENSIONS, SKIP_DIRECTORIES, MAX_FILE_SIZE
```

### 3. **Use Section Dividers for Structure**
```python
logger.section("Security Analysis", '=', 80)
logger.info("Scanning for vulnerabilities...")
# ... analysis ...
logger.section("", '=', 80)  # Closing divider
```

### 4. **Handle Errors Gracefully**
```python
try:
    # Risky operation
    result = analyze_file(file_path)
except Exception as e:
    logger.error(f"Failed to analyze {file_path}: {e}")
    logger.debug(f"Full traceback: {traceback.format_exc()}")
```

### 5. **Use Type Hints**
```python
from typing import List, Dict, Optional
from pathlib import Path

def process_files(files: List[Path]) -> Dict[str, int]:
    """Process files and return statistics"""
    stats = {}
    # ... processing ...
    return stats
```

---

## Migration Checklist

When refactoring a skill to use shared utilities:

- [ ] Add sys.path.insert boilerplate at top of file
- [ ] Import Logger and replace all print() statements
- [ ] Import constants and replace hardcoded values
- [ ] Create skill-specific constants.py if needed
- [ ] Replace manual file scanning with constants-based logic
- [ ] Add type hints to function signatures
- [ ] Add/update docstrings
- [ ] Test all functionality end-to-end
- [ ] Update skill's README with new architecture

---

## Version History

### v1.0.0 (2025-11-10)
- Initial release with Logger, constants_base, report_base, cli_utils
- Created during system-design-reviewer refactoring
- Supports cross-skill code reuse and consistency

---

## Support

For issues or questions about the shared utilities:

1. Check skill-specific documentation (e.g., `system-design-reviewer/README.md`)
2. Review the refactoring guide: `REFACTORING_GUIDE.md`
3. See example usage in `system-design-reviewer/scripts/`

---

## License

Part of Claude Skills project. Same license as parent repository.
