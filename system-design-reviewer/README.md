# System Design Reviewer

**Version**: 2.0.0 (Refactored)
**Purpose**: Automated system design analysis with architecture, security, performance, and cost optimization recommendations.

---

## Overview

The System Design Reviewer skill provides comprehensive automated analysis of software projects, generating professional reports with actionable recommendations across four key dimensions:

- 🏗️ **Architecture** - Design patterns, scalability, and best practices
- 🔒 **Security** - Vulnerability detection and security gaps
- ⚡ **Performance** - Bottleneck identification and optimization opportunities
- 💰 **Cost** - Cloud cost optimization and savings recommendations

---

## Quick Start

```bash
# Run complete system design review
python3 scripts/review_design.py /path/to/project --output report.html

# Run individual analyzers
python3 scripts/analyze_architecture.py /path/to/project
python3 scripts/security_analyzer.py /path/to/project
python3 scripts/performance_analyzer.py /path/to/project
python3 scripts/cost_optimizer.py /path/to/project

# Generate diagrams only
python3 scripts/generate_diagrams.py /path/to/project
```

---

## Architecture (v2.0)

### New Structure (Post-Refactoring)

```
system-design-reviewer/
├── README.md                          # This file
├── SKILL.md                           # Skill instructions & metadata
├── scripts/
│   ├── constants.py                   # Centralized patterns & config (176 lines)
│   ├── analyzer_base.py               # Abstract base class (280+ lines)
│   ├── report_generator.py            # HTML report generation (417 lines)
│   │
│   ├── review_design.py               # Main orchestrator (591 lines)
│   ├── analyze_architecture.py        # Architecture analysis (169 lines)
│   ├── security_analyzer.py           # Security analysis (231 lines)
│   ├── performance_analyzer.py        # Performance analysis (192 lines)
│   ├── cost_optimizer.py              # Cost optimization (249 lines)
│   └── generate_diagrams.py           # Diagram generation (231 lines)
│
└── [depends on]
    └── shared/                        # Cross-skill utilities
        ├── logger.py                  # Professional logging
        ├── constants_base.py          # Common configuration
        ├── report_base.py             # Report base classes
        └── cli_utils.py               # CLI utilities
```

### Key Design Patterns

#### 1. **BaseAnalyzer Pattern**

All analyzers inherit from `BaseAnalyzer` abstract base class:

```python
from analyzer_base import BaseAnalyzer

class MyAnalyzer(BaseAnalyzer):
    """Specific analyzer implementation"""

    def analyze(self) -> Dict:
        """Run analysis - must be implemented"""
        self._log_analysis_start("My Analysis")
        # ... analysis logic using base class helpers ...
        self._log_analysis_complete(results)
        return results

    def _find_strengths(self) -> List[str]:
        """Find positive aspects - must be implemented"""
        return ["strength1", "strength2"]
```

**Inherited Helper Methods** (15+ methods):
- `_get_code_files()` - Get all code files with extension filtering
- `_find_files_by_pattern()` - Glob-based file search
- `_read_file_safe()` - Safe file reading with error handling
- `_contains_technology()` - Technology indicator detection
- `_create_issue()` - Standardized issue dictionary creation
- `_should_skip_file()` - Check if file should be skipped
- `_log_analysis_start()` - Consistent analysis start logging
- `_log_analysis_complete()` - Consistent analysis completion logging

#### 2. **Centralized Configuration**

All detection patterns and thresholds in `constants.py`:

```python
# Security patterns
SECRET_PATTERNS = {
    "api_key": r'(?i)(api[_-]?key|apikey)\s*=\s*[\'"]([a-zA-Z0-9]{20,})[\'"]',
    "password": r'(?i)(password|passwd|pwd)\s*=\s*[\'"](?!{{)[^\'"]{8,}[\'"]',
    # ... more patterns ...
}

# Architecture indicators
ARCHITECTURE_INDICATORS = {
    'microservices': ['microservice', 'service-mesh', 'k8s'],
    'caching': ['redis', 'memcache', 'cache'],
    # ... more indicators ...
}
```

**Benefits**:
- Single source of truth for all patterns
- Easy to add/modify detection rules
- No duplicate pattern definitions

---

## Components

### 1. Main Orchestrator (`review_design.py`)

Coordinates all analyzers and generates comprehensive reports.

**Usage**:
```bash
# HTML report (default)
python3 review_design.py /path/to/project --output report.html

# Markdown report
python3 review_design.py /path/to/project --output report.md
```

**Process Flow**:
1. Generate architecture diagrams (Mermaid + ASCII)
2. Run architecture analysis
3. Run security analysis
4. Run performance analysis
5. Run cost analysis
6. Generate HTML report (or markdown fallback)

---

### 2. Architecture Analyzer

**Detects**: Microservices, message queues, database replication, caching, load balancers, CI/CD, monitoring

**Example Output**:
```json
{
  "issue_count": 4,
  "strengths": ["Database connection pooling"],
  "high_issues": [{"title": "No database replication", "effort": "4 hours"}]
}
```

---

### 3. Security Analyzer

**Scans For**: Hardcoded secrets, missing rate limiting, SQL injection, security headers, CSRF protection

**Example Output**:
```json
{
  "critical_count": 0,
  "high_count": 2,
  "strengths": ["Using HTTPS", "Secure password hashing"]
}
```

---

### 4. Performance Analyzer

**Analyzes**: Caching, N+1 queries, database indexes, async processing, CDN, compression

**Example Output**:
```json
{
  "optimization_count": 4,
  "high_impact": [{"title": "Add Redis caching", "expected": "10x faster"}]
}
```

---

### 5. Cost Optimizer

**Evaluates**: Over-provisioned instances, serverless opportunities, database sizing, reserved instances

**Example Output**:
```json
{
  "current_cost": 450,
  "optimized_cost": 340,
  "potential_savings_pct": 24
}
```

---

### 6. Diagram Generator

**Generates**: Architecture diagrams (Mermaid + ASCII), sequence diagrams, ER diagrams

---

## Refactoring Summary

### What Changed (v1.0 → v2.0)

| Aspect | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Code Duplication** | ~500 lines | 0 lines | 100% elimination |
| **Logging** | 22+ print() | Logger | Consistent |
| **Configuration** | Hardcoded | Centralized | Maintainable |
| **Reports** | Markdown | HTML + Markdown | Professional |

### Benefits

✅ **Maintainability**: Update detection logic in one place
✅ **Consistency**: All analyzers use same patterns
✅ **Extensibility**: New analyzers inherit 15+ helpers
✅ **Professional Output**: Colored console + HTML reports

---

## Development

### Validation

```bash
cd ../skill-creator/scripts
python package_skill.py ../../system-design-reviewer
```

### Testing

```bash
cd scripts/
python3 analyze_architecture.py /tmp/test-project
python3 review_design.py ~/Projects/my-app --output /tmp/review.html
```

---

## Troubleshooting

### Import Errors

```python
# Add sys.path.insert at top of script
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
```

### No Issues Detected

- Check file structure matches expected patterns
- Review detection patterns in `constants.py`
- Verify file extensions in CODE_EXTENSIONS

---

## Contributing

When contributing:

1. **Follow BaseAnalyzer pattern** - Inherit from base class
2. **Use shared utilities** - Logger, constants, report generators
3. **Add tests** - Unit tests for new analyzers
4. **Update constants** - Add patterns to constants.py
5. **Document changes** - Update this README

---

## License

Apache-2.0

---

**Questions?** See `/shared/README.md` for utilities documentation or `REFACTORING_GUIDE.md` for extending this pattern.
