#!/usr/bin/env python3
"""
Constants and Configuration for issue-manager
Centralized enums, dataclasses, and keywords.
"""

import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from constants_base import DEFAULT_TIMEOUT

# ===================================================================
# PLATFORM ENUMS
# ===================================================================

class Platform(Enum):
    """Supported issue tracking platforms."""
    LINEAR = "linear"
    GITHUB = "github"
    JIRA = "jira"


class IssueRelationship(Enum):
    """Types of relationships between issues."""
    BLOCKS = "blocks"
    BLOCKED_BY = "blocked-by"
    RELATES_TO = "relates-to"
    DUPLICATE = "duplicate"
    SUBTASK = "subtask"
    FOLLOW_UP = "follow-up"
    PREREQUISITE = "prerequisite"


# ===================================================================
# DATACLASSES
# ===================================================================

@dataclass
class Blocker:
    """Represents a blocking issue or dependency."""
    description: str
    category: str  # external, technical, resource
    impact: str  # high, medium, low
    context: str
    blocking_issue_id: Optional[str] = None
    eta: Optional[str] = None
    reported_at: str = None
    blocked_since: datetime = None

    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.reported_at is None:
            self.reported_at = datetime.now().isoformat()
        if self.blocked_since is None:
            self.blocked_since = datetime.now()


# ===================================================================
# ASSIGNMENT KEYWORDS
# ===================================================================

# Keywords that suggest human intervention is needed
HUMAN_KEYWORDS = [
    "approve", "approval",
    "decision", "decide",
    "review stakeholder", "stakeholder review",
    "negotiate", "negotiation",
    "business decision", "strategic decision",
    "prioritize", "priority",
    "strategic", "strategy",
    "policy", "compliance",
    "legal", "contract"
]

# Keywords that suggest agent can handle
AGENT_KEYWORDS = [
    "automate", "automated",
    "script", "scripted",
    "test", "testing",
    "lint", "linting",
    "format", "formatting",
    "refactor", "refactoring",
    "fix bug", "bugfix",
    "update dependency", "dependency update"
]

# ===================================================================
# BLOCKER CONFIGURATION
# ===================================================================

# Valid blocker categories
BLOCKER_CATEGORIES = ["external", "technical", "resource", "unknown"]

# Valid blocker impact levels
BLOCKER_IMPACTS = ["high", "medium", "low"]

# Default escalation threshold (in days)
DEFAULT_ESCALATION_THRESHOLD_DAYS = 3

# ===================================================================
# ISSUE SPLIT STRATEGIES
# ===================================================================

# Strategies for splitting large issues
SPLIT_STRATEGIES = [
    "acceptance-criteria",  # Split by acceptance criteria
    "functionality",        # Split by functional areas
    "layer"                 # Split by architectural layer (frontend/backend/db)
]

# Default number of subtasks when splitting
DEFAULT_SUBTASKS = 3

# Maximum recommended hours before suggesting split
MAX_ISSUE_HOURS = 16

# ===================================================================
# ISSUE PRIORITIES
# ===================================================================

PRIORITY_LEVELS = ["critical", "high", "medium", "low"]

# Priority mappings for different platforms
PRIORITY_MAP = {
    "linear": {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3
    },
    "github": {
        "critical": "critical",
        "high": "high",
        "medium": "medium",
        "low": "low"
    }
}

# ===================================================================
# DRY RUN CONFIGURATION
# ===================================================================

# Prefix for dry-run messages
DRY_RUN_PREFIX = "[DRY RUN]"

# ===================================================================
# CRITICAL PATH CONFIGURATION
# ===================================================================

# Minimum number of items to show critical path
MIN_CRITICAL_PATH_ITEMS = 1

# Default hours for critical path calculation
DEFAULT_TASK_HOURS = 2

# ===================================================================
# QUERY DEFAULTS
# ===================================================================

# Default query limit
DEFAULT_QUERY_LIMIT = 50

# Default sort order
DEFAULT_SORT_ORDER = "updated:desc"

# Valid sort fields
VALID_SORT_FIELDS = ["created", "updated", "priority", "status"]

# ===================================================================
# RELATIONSHIP DESCRIPTIONS
# ===================================================================

RELATIONSHIP_DESCRIPTIONS = {
    "blocks": "This issue blocks",
    "blocked-by": "This issue is blocked by",
    "relates-to": "This issue relates to",
    "duplicate": "This issue duplicates",
    "subtask": "This is a subtask of",
    "follow-up": "This is a follow-up to",
    "prerequisite": "This is a prerequisite for"
}

# ===================================================================
# STATUS TRANSITIONS
# ===================================================================

# Valid issue statuses
ISSUE_STATUSES = ["open", "in_progress", "blocked", "closed", "cancelled"]

# Status transition rules
VALID_TRANSITIONS = {
    "open": ["in_progress", "blocked", "cancelled"],
    "in_progress": ["blocked", "closed", "open"],
    "blocked": ["in_progress", "open", "cancelled"],
    "closed": ["open"],
    "cancelled": ["open"]
}

# ===================================================================
# LABELS
# ===================================================================

# Common labels for issue categorization
COMMON_LABELS = [
    "bug",
    "feature",
    "enhancement",
    "documentation",
    "needs-review",
    "blocked",
    "high-priority",
    "technical-debt"
]

# Labels to preserve when splitting issues
PRESERVE_LABELS = ["project:", "team:", "area:"]

# ===================================================================
# NOTIFICATION SETTINGS
# ===================================================================

# Default notification behavior
DEFAULT_NOTIFY_ASSIGNEE = True
DEFAULT_NOTIFY_WATCHERS = False

# ===================================================================
# ERROR MESSAGES
# ===================================================================

ERROR_MESSAGES = {
    "missing_issue": "Error: --issue required",
    "missing_blocker": "Error: --issue and --blocked-by required",
    "missing_resolution": "Error: --issue and --resolution required",
    "missing_filter": "Error: --filter required",
    "missing_source": "Error: --source, --type, and --title required",
    "missing_assignee": "Error: --issue and --assignee required",
    "missing_reassign": "Error: --issue, --from-assignee, and --to-assignee required",
    "missing_merge": "Error: --issues and --keep required",
    "invalid_threshold": "Error: Invalid threshold format (use format like '3d' or '1w')"
}

# ===================================================================
# SUCCESS ICONS
# ===================================================================

# Icons for different operations
ICONS = {
    "success": "✓",
    "error": "✗",
    "warning": "⚠️",
    "blocked": "🚫",
    "info": "📊",
    "critical_path": "🎯",
    "suggestion": "💡",
    "agent": "🤖",
    "human": "👤"
}
