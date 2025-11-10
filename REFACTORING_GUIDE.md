# Claude Skills - Refactoring Guide

**Version**: 1.0.0
**Purpose**: Step-by-step guide for refactoring skills to use shared utilities and eliminate code duplication.

---

## Overview

This guide provides a systematic approach to refactoring Claude Skills to use the shared utilities library, eliminate code duplication, and improve maintainability.

**Prerequisites**:
- Shared utilities library exists (`/shared` directory)
- Familiarity with Python and the skill being refactored
- Git repository for version control

---

## When to Use This Guide

Use this guide when:

- ✅ Refactoring an existing skill to use shared utilities
- ✅ Eliminating code duplication across scripts
- ✅ Standardizing console output with Logger
- ✅ Adding professional HTML reports
- ✅ Improving maintainability and consistency

---

## Refactoring Process Overview

```
1. Analysis (1-2 hours)
   ↓
2. Planning (1 hour)
   ↓
3. Create Infrastructure (2-3 hours)
   ↓
4. Refactor Scripts (3-4 hours)
   ↓
5. Testing (1-2 hours)
   ↓
6. Documentation (1-2 hours)
   ↓
7. Commit & Release
```

**Total Estimated Time**: 8-15 hours per skill

---

## Phase 1: Analysis

### Step 1.1: Identify Code Duplication

Run analysis to find duplicate patterns:

```bash
# Find file scanning patterns
grep -r "for root, dirs, files in os.walk" skill-name/

# Find print statements
grep -r "print(" skill-name/ | wc -l

# Find hardcoded patterns
grep -r "redis\|memcache\|cache" skill-name/

# Find similar functions across files
cd skill-name/scripts
for f in *.py; do echo "=== $f ==="; grep "^def " $f; done
```

**Document Findings**:
- Number of print() statements: ___
- Duplicate helper methods: ___
- Hardcoded patterns/constants: ___
- Similar code blocks: ___

### Step 1.2: Identify Architecture Pattern

Determine which pattern fits best:

#### Pattern A: BaseAnalyzer (for analysis/scanning skills)

**Use when**:
- Multiple analyzer scripts
- Common file scanning logic
- Technology detection patterns
- Issue/recommendation generation

**Examples**: system-design-reviewer, code-quality-checker

#### Pattern B: Simple Utilities (for simpler skills)

**Use when**:
- Few scripts
- Minimal code duplication
- Primarily logger integration needed

**Examples**: task-decomposer, issue-manager

#### Pattern C: Template-Based (for generation skills)

**Use when**:
- Generating code/files
- Template management
- Minimal analysis logic

**Examples**: skill-creator

**Decision**: I will use Pattern ___ for skill-name

### Step 1.3: Review Current Structure

Document current architecture:

```bash
skill-name/
├── scripts/
│   ├── script1.py (XX lines)
│   ├── script2.py (XX lines)
│   └── script3.py (XX lines)
└── README.md
```

**Current Metrics**:
- Total scripts: ___
- Total lines of code: ___
- Duplicate code estimate: ___
- Print statements: ___

---

## Phase 2: Planning

### Step 2.1: Define New Structure

Plan the refactored structure:

```bash
skill-name/
├── README.md                    # Updated documentation
├── scripts/
│   ├── constants.py             # NEW: Centralized patterns
│   ├── [analyzer_base.py]       # OPTIONAL: Base class
│   ├── [report_generator.py]    # OPTIONAL: HTML reports
│   ├── script1.py               # REFACTORED
│   ├── script2.py               # REFACTORED
│   └── script3.py               # REFACTORED
└── [depends on] /shared/         # Shared utilities
```

### Step 2.2: Create Task List

```markdown
- [ ] Create skill-name/scripts/constants.py
- [ ] Create skill-name/scripts/[base_class].py (if needed)
- [ ] Create skill-name/scripts/report_generator.py (if needed)
- [ ] Refactor script1.py
- [ ] Refactor script2.py
- [ ] Refactor script3.py
- [ ] Test all scripts individually
- [ ] Test integration
- [ ] Update README.md
- [ ] Create refactoring summary
- [ ] Git commit
```

### Step 2.3: Estimate Impact

| Metric | Before | After (Est.) | Improvement |
|--------|--------|--------------|-------------|
| **Total LOC** | ___ | ___ | -___% |
| **Duplicate Code** | ___ lines | 0 lines | -100% |
| **Print Statements** | ___ | 0 | -100% |
| **Report Formats** | Markdown | HTML + MD | +1 format |

---

## Phase 3: Create Infrastructure

### Step 3.1: Create constants.py

Create `skill-name/scripts/constants.py`:

```python
#!/usr/bin/env python3
"""
Constants and configuration for skill-name
Centralized patterns and thresholds.
"""

import sys
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from constants_base import *

# ===================================================================
# SKILL-SPECIFIC PATTERNS
# ===================================================================

# Technology indicators
TECHNOLOGY_PATTERNS = {
    'framework_name': ['indicator1', 'indicator2', 'file.ext'],
    'library_name': ['lib', 'library', 'package'],
}

# Detection patterns (regex)
DETECTION_PATTERNS = {
    'pattern_type': r'regex_pattern_here',
}

# Thresholds
MIN_FILE_SIZE = 100  # bytes
MAX_COMPLEXITY = 10
PERFORMANCE_THRESHOLD = 0.5  # seconds

# File patterns
INCLUDE_PATTERNS = ['*.py', '*.js']
EXCLUDE_PATTERNS = ['*.test.py', '*.spec.js']
```

### Step 3.2: Create Base Class (if Pattern A)

Create `skill-name/scripts/analyzer_base.py`:

```python
#!/usr/bin/env python3
"""
Base analyzer class for skill-name
Provides common functionality for all analyzers.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from logger import Logger
from constants_base import CODE_EXTENSIONS, SKIP_DIRECTORIES

from constants import TECHNOLOGY_PATTERNS


class BaseSkillAnalyzer(ABC):
    """Abstract base class for all skill analyzers"""

    def __init__(self, project_path: str):
        """Initialize analyzer with project path"""
        self.project_path = Path(project_path).resolve()
        self.logger = Logger()

    @abstractmethod
    def analyze(self) -> Dict:
        """
        Run the analysis

        Returns:
            Dict containing analysis results
        """
        pass

    @abstractmethod
    def _find_strengths(self) -> List[str]:
        """
        Find positive aspects

        Returns:
            List of strength descriptions
        """
        pass

    # ============================================================
    # HELPER METHODS (Shared by all analyzers)
    # ============================================================

    def _get_code_files(self, extensions: Optional[List[str]] = None) -> List[Path]:
        """Get all code files in the project"""
        if extensions is None:
            extensions = CODE_EXTENSIONS

        files = []
        for ext in extensions:
            for file_path in self.project_path.rglob(f'*{ext}'):
                if not self._should_skip_file(file_path):
                    files.append(file_path)
        return files

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        # Check if in skip directory
        for skip_dir in SKIP_DIRECTORIES:
            if skip_dir in file_path.parts:
                return True
        return False

    def _read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read file contents with error handling"""
        try:
            return file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            self.logger.debug(f"Failed to read {file_path}: {e}")
            return None

    def _contains_technology(self, tech_indicators: List[str]) -> bool:
        """Check if project uses specified technology"""
        code_files = self._get_code_files()

        for file_path in code_files:
            content = self._read_file_safe(file_path)
            if content:
                content_lower = content.lower()
                if any(indicator in content_lower for indicator in tech_indicators):
                    return True
        return False

    def _log_analysis_start(self, analysis_type: str) -> None:
        """Log analysis start with standard formatting"""
        self.logger.section(f"{analysis_type} Analysis", '=', 60)
        self.logger.info(f"Project: {self.project_path}")

    def _log_analysis_complete(self, results: Dict) -> None:
        """Log analysis completion with key metrics"""
        self.logger.success("Analysis complete!")
        issue_count = results.get('issue_count', results.get('optimization_count', 0))
        self.logger.info(f"Found {issue_count} items to review")
```

### Step 3.3: Create Report Generator (if needed)

Create `skill-name/scripts/report_generator.py`:

```python
#!/usr/bin/env python3
"""
Report generator for skill-name
Generates professional HTML reports.
"""

import sys
from pathlib import Path
from typing import Dict, Optional

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from report_base import HTMLReportBase


class SkillReportGenerator(HTMLReportBase):
    """Generate professional HTML reports for skill analysis"""

    def __init__(self, title: str = "Skill Analysis Report"):
        super().__init__(title)

    def generate(self) -> str:
        """Generate the complete report"""
        return self.build()

    # Add custom report sections here
    def add_custom_section(self, data: Dict) -> None:
        """Add custom section to report"""
        html = f"""
        <div class="section">
            <h2>Custom Section</h2>
            <!-- Your custom HTML here -->
        </div>
        """
        self.add_section(html)
```

---

## Phase 4: Refactor Scripts

### Step 4.1: Update Imports

**Before**:
```python
#!/usr/bin/env python3
import os
from pathlib import Path

def main():
    print("Starting analysis...")
```

**After**:
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from logger import Logger

# Import skill-specific utilities
from constants import TECHNOLOGY_PATTERNS
from analyzer_base import BaseSkillAnalyzer  # If using base class

def main():
    logger = Logger()
    logger.info("Starting analysis...")
```

### Step 4.2: Replace Print Statements

**Before**:
```python
print("Starting analysis...")
print(f"Found {count} issues")
print("✅ Complete!")
```

**After**:
```python
logger.info("Starting analysis...")
logger.info(f"Found {count} issues")
logger.success("Complete!")
```

**Mapping**:
- `print("message")` → `logger.info("message")`
- `print("✅ ...")` → `logger.success("...")`
- `print("⚠️ ...")` → `logger.warning("...")`
- `print("❌ ...")` → `logger.error("...")`

### Step 4.3: Extract Hardcoded Constants

**Before**:
```python
def check_technology():
    indicators = ['redis', 'memcache', 'cache']
    for file in files:
        content = file.read_text()
        if any(ind in content.lower() for ind in indicators):
            return True
```

**After** (in constants.py):
```python
CACHING_INDICATORS = ['redis', 'memcache', 'cache']
```

**After** (in script):
```python
from constants import CACHING_INDICATORS

def check_technology():
    return self._contains_technology(CACHING_INDICATORS)
```

### Step 4.4: Use Base Class (if applicable)

**Before**:
```python
class MyAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)

    def analyze(self):
        # ... analysis logic ...
        pass

    def _scan_files(self):
        # 30 lines of file scanning code
        pass
```

**After**:
```python
from analyzer_base import BaseSkillAnalyzer

class MyAnalyzer(BaseSkillAnalyzer):
    """Analyze specific aspects of the project"""

    def analyze(self):
        self._log_analysis_start("My Analysis")
        # ... analysis logic using inherited helpers ...
        self._log_analysis_complete(results)
        return results

    def _find_strengths(self):
        return ["Strength 1", "Strength 2"]

    # No need for _scan_files - use inherited _get_code_files()
```

### Step 4.5: Update Error Handling

**Before**:
```python
try:
    content = file.read_text()
except Exception:
    pass  # Silent failure
```

**After**:
```python
content = self._read_file_safe(file)
if not content:
    self.logger.debug(f"Skipped {file}: unreadable")
    continue
```

---

## Phase 5: Testing

### Step 5.1: Unit Test Each Script

```bash
# Test each script individually
cd skill-name/scripts/

python3 script1.py /tmp/test-project
python3 script2.py /tmp/test-project
python3 script3.py /tmp/test-project
```

**Checklist**:
- [ ] Script runs without errors
- [ ] Output uses Logger (colored if TTY)
- [ ] No print() statements visible
- [ ] Results are accurate
- [ ] Error handling works

### Step 5.2: Integration Test

```bash
# Test main orchestrator or workflow
python3 main_script.py /tmp/test-project --output /tmp/report.html

# Verify output
ls -lh /tmp/report.html
open /tmp/report.html  # macOS
```

**Checklist**:
- [ ] All scripts work together
- [ ] No import errors
- [ ] Reports generate correctly
- [ ] Performance acceptable

### Step 5.3: Edge Case Testing

```bash
# Test with minimal project
mkdir /tmp/empty-project
python3 script.py /tmp/empty-project

# Test with large project
python3 script.py ~/Projects/large-codebase

# Test with errors
python3 script.py /nonexistent/path
```

---

## Phase 6: Documentation

### Step 6.1: Update README.md

Update `skill-name/README.md` with:

1. **Version number** - Bump to v2.0.0
2. **Architecture section** - Show new structure
3. **Usage examples** - With new command-line options
4. **Refactoring summary** - Before/after metrics
5. **Dependencies** - Note shared utilities dependency

See `/system-design-reviewer/README.md` as example.

### Step 6.2: Create Refactoring Summary

Create comprehensive summary document:

```bash
# Create summary
touch /tmp/qa-refactor/SKILLNAME_REFACTORING_SUMMARY.md
```

Include:
- Executive summary
- Quantitative results
- Architecture changes
- File-by-file changes
- Test results
- Benefits realized

See `/tmp/qa-refactor/SYSTEM_DESIGN_REVIEWER_REFACTORING_SUMMARY.md` as example.

### Step 6.3: Update REFACTORING_PROGRESS.md

Add entry to master progress tracker:

```markdown
## Skill X: skill-name ✅

### Summary
Brief description of skill

### Refactoring Details
Date, files changed, code eliminated

### Test Results
All tests passing

### Git Commit
Commit hash and message
```

---

## Phase 7: Commit & Release

### Step 7.1: Git Commit

```bash
cd /path/to/claude-skills

# Stage all changes
git add shared/ skill-name/

# Check what's staged
git status

# Create comprehensive commit
git commit -m "$(cat <<'EOF'
Refactor skill-name to use shared utilities and eliminate code duplication

Major architectural improvements to skill-name skill:

- Created [infrastructure files]
- Refactored X scripts to use [BaseClass/Logger/etc]
- Eliminated ~XXX lines of duplicate code
- Centralized all patterns in constants.py
- Added professional HTML report generation

Technical Details:
- script1.py: XXX→YYY lines (change description)
- script2.py: XXX→YYY lines (change description)
- ...

New Infrastructure:
- shared/[files if first refactoring]
- skill-name/scripts/constants.py (XXX lines)
- skill-name/scripts/[base_class].py (XXX lines)
- ...

Benefits:
✅ Zero code duplication
✅ Consistent logging
✅ Professional reports
✅ Easier maintenance
✅ All tests passing

Next: [Next skill name]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 7.2: Verify Commit

```bash
# Review commit
git show HEAD

# Check file changes
git diff HEAD~1 --stat

# Verify all tests still pass
cd skill-name/scripts/
./run_tests.sh  # Or your test command
```

### Step 7.3: Tag Release (optional)

```bash
# Tag the refactored version
git tag -a skill-name-v2.0.0 -m "Refactored version with shared utilities"

# Push commit and tag
git push origin main
git push origin skill-name-v2.0.0
```

---

## Common Patterns

### Pattern: File Scanning

**Before** (30 lines, duplicated):
```python
files = []
for root, dirs, files_list in os.walk(project_path):
    # Remove node_modules
    if 'node_modules' in dirs:
        dirs.remove('node_modules')
    # Remove .git
    if '.git' in dirs:
        dirs.remove('.git')

    for file in files_list:
        if file.endswith(('.py', '.js', '.ts')):
            file_path = Path(root) / file
            if file_path.stat().st_size < 10 * 1024 * 1024:
                files.append(file_path)
```

**After** (1 line):
```python
files = self._get_code_files(['.py', '.js', '.ts'])
```

---

### Pattern: Technology Detection

**Before** (20 lines, duplicated):
```python
def has_redis():
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.py', '.js', '.yml')):
                try:
                    content = Path(root, file).read_text()
                    if 'redis' in content.lower():
                        return True
                except:
                    pass
    return False
```

**After** (1 line):
```python
def has_redis():
    return self._contains_technology(['redis'])
```

---

### Pattern: Issue Creation

**Before** (inconsistent):
```python
issue = {
    "name": "Issue Title",
    "desc": "Description",
    "fix": "How to fix",
    "time": "2 hours"
}
```

**After** (consistent):
```python
issue = self._create_issue(
    title="Issue Title",
    impact="What's affected",
    recommendation="How to fix",
    effort="2 hours"
)
```

---

## Troubleshooting

### Import Error: ModuleNotFoundError

**Problem**: `ModuleNotFoundError: No module named 'logger'`

**Solution**:
```python
# Add to top of every script
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
```

### Logger Not Showing Colors

**Problem**: Output is not colored

**Causes**:
1. Output redirected to file
2. Not running in TTY
3. NO_COLOR environment variable set

**Solution**: Colors automatic, check TTY with `python3 -c "import sys; print(sys.stdout.isatty())"`

### Base Class Not Found

**Problem**: `ModuleNotFoundError: No module named 'analyzer_base'`

**Solution**: Ensure script is in `skill-name/scripts/` and base class exists

---

## Checklist

Use this checklist for each skill refactoring:

### Analysis
- [ ] Counted print() statements
- [ ] Identified duplicate code
- [ ] Listed hardcoded constants
- [ ] Determined architecture pattern
- [ ] Reviewed current structure

### Infrastructure
- [ ] Created constants.py
- [ ] Created base class (if needed)
- [ ] Created report generator (if needed)
- [ ] Tested infrastructure files

### Refactoring
- [ ] Updated all imports
- [ ] Replaced all print() statements
- [ ] Extracted hardcoded constants
- [ ] Applied base class pattern
- [ ] Improved error handling

### Testing
- [ ] Unit tested each script
- [ ] Integration tested workflow
- [ ] Edge case testing
- [ ] Performance validation

### Documentation
- [ ] Updated README.md
- [ ] Created refactoring summary
- [ ] Updated REFACTORING_PROGRESS.md
- [ ] Added code comments

### Release
- [ ] Git commit created
- [ ] Commit message comprehensive
- [ ] All tests passing
- [ ] Tag created (optional)

---

## Success Metrics

A successful refactoring achieves:

- ✅ **Zero print() statements** - All use Logger
- ✅ **Zero duplicate code** - Shared utilities or base class
- ✅ **Centralized configuration** - Constants in one place
- ✅ **Professional output** - Colored logging + HTML reports
- ✅ **Improved maintainability** - DRY principles
- ✅ **All tests passing** - No regressions
- ✅ **Documentation complete** - README + summary

---

## Getting Help

If you encounter issues:

1. **Review examples** - Check system-design-reviewer refactoring
2. **Check shared/README.md** - Utilities documentation
3. **Review REFACTORING_PROGRESS.md** - See completed examples
4. **Ask questions** - Document blockers for resolution

---

## Appendix: Template Files

### Template: constants.py

See section "Step 3.1: Create constants.py" above

### Template: analyzer_base.py

See section "Step 3.2: Create Base Class" above

### Template: report_generator.py

See section "Step 3.3: Create Report Generator" above

---

## License

Part of Claude Skills project. Same license as parent repository.

---

**Version**: 1.0.0
**Last Updated**: 2025-11-10
**Next Review**: After 5 skills refactored
