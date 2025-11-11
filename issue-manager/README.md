# Issue Manager

Comprehensive issue management operations including assignment, blocking relationships, splitting, critical path analysis, and intelligent agent/human assignment detection across Linear, GitHub, and Jira.

## Overview

Streamline issue tracking workflows with automated operations, dependency analysis, and smart assignment recommendations. Supports multiple platforms with unified interface and professional output.

### Key Features

- **Smart Assignment** - AI/human detection based on task keywords
- **Block Analysis** - Identify blocking issues and dependencies
- **Critical Path** - Calculate project bottlenecks and priorities
- **Auto-Escalation** - Detect stale issues requiring attention
- **Issue Splitting** - Break large issues into manageable subtasks
- **Multi-Platform** - Linear, GitHub, and Jira support
- **Dry-Run Mode** - Preview operations before execution
- **Professional Logging** - Colored console output with icons

## Architecture

### Scripts

| Script | Purpose | Lines |
|--------|---------|-------|
| `issue_operations.py` | CRUD operations and workflows | 580 |
| `analyze_blocks.py` | Dependency and critical path analysis | 304 |
| `constants.py` | Centralized configuration | 263 |

**Total**: 1,147 lines of Python

### Technology Stack

- **Python 3.8+** - Core language
- **Logger** - Professional colored output (from shared utilities)
- **Dataclasses** - Type-safe issue representation
- **Enum Types** - Platform and relationship types

## Installation

### Prerequisites

```bash
# Python 3.8 or higher
python3 --version

# No external dependencies required (uses stdlib + shared logger)
```

### Platform API Setup

Configure API keys for your platform(s):

```bash
# Linear
export LINEAR_API_KEY="lin_api_..."

# GitHub
export GITHUB_TOKEN="ghp_..."

# Jira
export JIRA_API_KEY="your_key_here"
export JIRA_DOMAIN="yourcompany.atlassian.net"
```

## Usage

### Issue Assignment

```bash
cd scripts

# Assign issue to specific person
python3 issue_operations.py assign \
  --issue ISSUE-123 \
  --assignee john@example.com

# Auto-assign based on task type (AI vs human detection)
python3 issue_operations.py auto-assign --issue ISSUE-456

# Reassign from one person to another
python3 issue_operations.py reassign \
  --issue ISSUE-789 \
  --from-assignee alice@example.com \
  --to-assignee bob@example.com

# Preview assignment (dry-run)
python3 issue_operations.py assign \
  --issue ISSUE-123 \
  --assignee john@example.com \
  --dry-run
```

### Block Management

```bash
# Report a blocking issue
python3 issue_operations.py report-blocker \
  --issue ISSUE-123 \
  --blocked-by ISSUE-456 \
  --description "Waiting for API implementation"

# Resolve a blocker
python3 issue_operations.py resolve-blocker \
  --issue ISSUE-123 \
  --resolution "API completed and merged"

# Analyze blocking relationships
python3 analyze_blocks.py --issue ISSUE-123
```

### Critical Path Analysis

```bash
# Find critical path items in project
python3 analyze_blocks.py \
  --critical-path \
  --project "Web App Refactor"

# Auto-escalate stale issues
python3 analyze_blocks.py --auto-escalate

# Custom escalation threshold
python3 analyze_blocks.py \
  --auto-escalate \
  --threshold-days 5
```

### Issue Splitting

```bash
# Split large issue into subtasks
python3 issue_operations.py split-issue \
  --issue REFACTOR-2025 \
  --num-subtasks 4

# Create subtasks from description
python3 issue_operations.py split-issue \
  --issue FEATURE-100 \
  --subtasks "Database schema" "API endpoints" "Frontend UI" "Tests"
```

### Advanced Operations

```bash
# Merge duplicate issues
python3 issue_operations.py merge-issues \
  --issues ISSUE-1 ISSUE-2 ISSUE-3 \
  --keep ISSUE-1

# Link related issues
python3 issue_operations.py link-issues \
  --issue ISSUE-123 \
  --related-to ISSUE-456 \
  --relationship "relates-to"

# Bulk update labels
python3 issue_operations.py bulk-update \
  --filter "status:open priority:high" \
  --add-label "urgent"
```

## Operations Reference

### Core Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| **assign** | `assign --issue X --assignee Y` | Assign issue to user |
| **auto-assign** | `auto-assign --issue X` | AI/human detection |
| **reassign** | `reassign --issue X --from Y --to Z` | Transfer ownership |
| **report-blocker** | `report-blocker --issue X --blocked-by Y` | Mark blocking dependency |
| **resolve-blocker** | `resolve-blocker --issue X --resolution R` | Clear blocker |
| **split-issue** | `split-issue --issue X --num-subtasks N` | Create subtasks |
| **merge-issues** | `merge-issues --issues X Y Z --keep X` | Merge duplicates |
| **link-issues** | `link-issues --issue X --related-to Y` | Create relationship |
| **bulk-update** | `bulk-update --filter F --add-label L` | Mass operations |
| **create-from-template** | `create-from-template --source S --type T` | Template creation |

### Analysis Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| **analyze** | `analyze_blocks.py --issue X` | Dependency analysis |
| **critical-path** | `analyze_blocks.py --critical-path --project P` | Find bottlenecks |
| **auto-escalate** | `analyze_blocks.py --auto-escalate` | Stale issue detection |
| **suggest-split** | `analyze_blocks.py --suggest-split --issue X` | Split recommendations |

## Output Examples

### Auto-Assignment Output

```
[*] Analyzing issue: TASK-456

Task Type Detection:
  Title: "Design authentication user flow"
  Keywords Found: design, user experience

[*] 👤 Task assigned to: HUMAN
[*] Reason: Design and UX work requires human judgment

[✓] Assignment recommendation: alice@example.com (UX Designer)
```

### Block Analysis Output

```
[*] Analyzing issue: ISSUE-123

[!] Found 2 blocker(s):

  🚫 BLOCKER #1
     Issue: ISSUE-456 (API Implementation)
     Impact: HIGH
     Blocked Since: 2025-11-08
     ETA: 2025-11-15

  🚫 BLOCKER #2
     Issue: ISSUE-789 (Database Migration)
     Impact: MEDIUM
     Blocked Since: 2025-11-10

📊 Critical path items:
  1. 🎯 ISSUE-456 (blocks 3 other issues)
  2. 🎯 ISSUE-789 (blocks 1 other issue)
```

### Split Issue Output

```
[*] Splitting issue: REFACTOR-2025

[✓] Created 4 subtasks:

  1. REFACTOR-2025-1: Analyze current architecture
     Assignee: 🔄 either
     Priority: P0 (Critical Path)

  2. REFACTOR-2025-2: Implement core refactoring
     Assignee: 🤖 agent
     Priority: P0 (Critical Path)
     Dependencies: #1

  3. REFACTOR-2025-3: Update tests and documentation
     Assignee: 🤖 agent
     Priority: P1 (Important)
     Dependencies: #2

  4. REFACTOR-2025-4: Code review and deployment
     Assignee: 👤 human
     Priority: P1 (Important)
     Dependencies: #3
```

## Assignment Intelligence

### AI-Suitable Tasks (🤖)

Auto-detected keywords:
- `implement`, `fix bug`, `refactor`, `optimize`
- `test`, `automate`, `script`, `build`
- `deploy`, `migrate`, `update dependency`

### Human-Required Tasks (👤)

Auto-detected keywords:
- `design`, `architecture`, `decision`, `strategy`
- `approve`, `review stakeholder`, `negotiate`
- `prioritize`, `policy`, `compliance`, `legal`

### Configurable in constants.py

```python
HUMAN_KEYWORDS = [
    "approve", "decision", "review stakeholder",
    "negotiate", "business decision", "prioritize",
    "strategic", "policy", "compliance", "legal"
]

AGENT_KEYWORDS = [
    "implement", "code", "program", "develop",
    "fix bug", "refactor", "test", "automate"
]
```

## Platform Support

### Linear

```python
from constants import Platform

manager = IssueManager(Platform.LINEAR)
manager.assign_issue("LIN-123", "user@example.com")
```

### GitHub

```python
manager = IssueManager(Platform.GITHUB)
manager.report_blocker(
    issue_id="123",
    blocked_by="456",
    description="Waiting for PR review"
)
```

### Jira

```python
manager = IssueManager(Platform.JIRA)
manager.split_issue("PROJ-100", num_subtasks=3)
```

## Configuration

### Environment Variables

```bash
# Platform selection (default: linear)
ISSUE_PLATFORM="linear"  # or "github", "jira"

# Escalation threshold (days before stale)
ESCALATION_THRESHOLD_DAYS=7

# Dry-run mode (preview only)
DRY_RUN=true
```

### constants.py

Customize behavior:

```python
# Platform enum
class Platform(Enum):
    LINEAR = "linear"
    GITHUB = "github"
    JIRA = "jira"

# Issue relationships
class IssueRelationship(Enum):
    BLOCKS = "blocks"
    BLOCKED_BY = "blocked-by"
    RELATES_TO = "relates-to"
    DUPLICATE = "duplicate"
    SUBTASK = "subtask"
    FOLLOW_UP = "follow-up"
    PREREQUISITE = "prerequisite"

# Blocker dataclass
@dataclass
class Blocker:
    description: str
    category: str  # external, technical, resource
    impact: str    # high, medium, low
    context: str
    blocking_issue_id: Optional[str] = None
    eta: Optional[str] = None
```

## Best Practices

### 1. Use Dry-Run Mode

Always preview operations before executing:

```bash
python3 issue_operations.py split-issue \
  --issue LARGE-TASK \
  --num-subtasks 5 \
  --dry-run
```

### 2. Document Blockers

Provide context when reporting blockers:

```bash
python3 issue_operations.py report-blocker \
  --issue ISSUE-123 \
  --blocked-by ISSUE-456 \
  --description "Waiting for API v2 migration. ETA: Nov 15. Contact: alice@example.com"
```

### 3. Regular Critical Path Analysis

Weekly bottleneck review:

```bash
# Monday morning routine
python3 analyze_blocks.py --critical-path --project "Sprint 42"
python3 analyze_blocks.py --auto-escalate
```

### 4. Leverage Auto-Assignment

Let the system recommend assignments:

```bash
# Review recommendations before committing
python3 issue_operations.py auto-assign --issue TASK-X --dry-run

# Then execute
python3 issue_operations.py auto-assign --issue TASK-X
```

## Troubleshooting

### Common Issues

**Problem**: "Issue not found"
```bash
# Verify issue ID format
# Linear: LIN-123, ABC-456
# GitHub: owner/repo#123
# Jira: PROJ-123
```

**Problem**: Assignment detection incorrect

**Solution**: Override keywords in `constants.py`:
```python
# Add domain-specific terms
HUMAN_KEYWORDS.append("architectural-review")
AGENT_KEYWORDS.append("database-optimization")
```

**Problem**: Dry-run mode not working

**Solution**: Use `--dry-run` flag explicitly:
```bash
python3 issue_operations.py assign --issue X --assignee Y --dry-run
```

## Development

### Project Structure

```
issue-manager/
├── SKILL.md                # Skill definition
├── README.md               # This file
└── scripts/
    ├── issue_operations.py # Main CRUD operations
    ├── analyze_blocks.py   # Dependency analysis
    └── constants.py        # Configuration and types
```

### Testing

```bash
# Test assignment
python3 issue_operations.py assign \
  --issue TEST-1 \
  --assignee test@example.com \
  --dry-run

# Test block analysis
python3 analyze_blocks.py \
  --issue TEST-1 \
  --dry-run

# Test critical path
python3 analyze_blocks.py \
  --critical-path \
  --project "Test Project"
```

### Extending

Add custom operations:

```python
# In issue_operations.py
class IssueManager:
    def custom_operation(self, issue_id: str, params: Dict):
        """Implement your custom logic"""
        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would execute custom operation")
            return

        # Execute operation
        self.logger.success(f"Custom operation completed for {issue_id}")
```

## Refactoring History

**Date**: 2025-11-11
**Changes**: Refactored to eliminate code duplication and standardize logging

- Replaced 122 print() statements with Logger
- Unified Blocker dataclass (was duplicated across both scripts)
- Centralized Platform and IssueRelationship enums
- Extracted HUMAN_KEYWORDS and AGENT_KEYWORDS to constants
- Standardized error messages and icons
- Professional colored console output

**See**: `/tmp/qa-refactor/ISSUE_MANAGER_REFACTORING_SUMMARY.md`

## License

Apache-2.0

## Support

- **Documentation**: See `SKILL.md` for detailed instructions
- **Shared Utilities**: See `../shared/README.md` for Logger documentation
- **Issue Tracker**: Report bugs via project repository

---

**Last Updated**: 2025-11-11
**Version**: 2.0.0 (Post-refactoring)
