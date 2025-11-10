#!/usr/bin/env python3
"""
Block Analysis Script

Analyze blocking issues and suggest unblocking strategies.

Refactored to use professional logging and centralized constants.

Usage:
    python analyze_blocks.py --issue ISSUE-123
    python analyze_blocks.py --issue ISSUE-456 --suggest-split
    python analyze_blocks.py --auto-escalate --threshold 3d

Examples:
    python analyze_blocks.py --issue ISSUE-123
    python analyze_blocks.py --suggest-split --issue ISSUE-456
    python analyze_blocks.py --critical-path --project my-project
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from logger import Logger

# Import constants
from constants import (
    Blocker,
    DEFAULT_ESCALATION_THRESHOLD_DAYS,
    SPLIT_STRATEGIES,
    DEFAULT_SUBTASKS,
    ICONS
)


@dataclass
class BlockerInfo:
    """Information about a blocking issue (extends Blocker with additional fields)."""
    blocker_id: str
    description: str
    category: str
    impact: str
    blocked_since: datetime
    eta: Optional[str] = None
    suggested_action: Optional[str] = None


class BlockAnalyzer:
    """Analyze blocking issues and dependencies."""

    def __init__(self, logger: Logger = None):
        """Initialize analyzer with optional logger."""
        self.issues_cache = {}
        self.logger = logger or Logger()

    def analyze_issue(self, issue_id: str) -> Dict:
        """Analyze blocking status of an issue."""

        self.logger.info(f"Analyzing issue: {issue_id}\n")

        # Example analysis (would use actual API)
        blockers = self._find_blockers(issue_id)
        transitive_deps = self._find_transitive_dependencies(issue_id)
        critical_path = self._calculate_critical_path(issue_id)

        if not blockers:
            self.logger.success("No direct blockers found")
        else:
            self.logger.warning(f"Found {len(blockers)} blocker(s):\n")
            for blocker in blockers:
                self._print_blocker(blocker)

        if transitive_deps:
            self.logger.info(f"\n{ICONS['info']} Transitive dependencies: {len(transitive_deps)}")
            for dep in transitive_deps[:3]:  # Show first 3
                self.logger.info(f"  → {dep}")

        if critical_path:
            self.logger.info(f"\n{ICONS['critical_path']} Critical path items:")
            for item in critical_path:
                self.logger.info(f"  → {item}")

        # Suggest unblocking strategies
        if blockers:
            self.logger.info(f"\n{ICONS['suggestion']} Suggested unblocking strategies:")
            for blocker in blockers:
                if blocker.suggested_action:
                    self.logger.info(f"  • {blocker.suggested_action}")

        return {
            "issue_id": issue_id,
            "blockers": [vars(b) for b in blockers],
            "transitive_dependencies": transitive_deps,
            "critical_path": critical_path
        }

    def suggest_split(self, issue_id: str) -> Dict:
        """Suggest how to split a complex issue."""

        self.logger.info(f"Analyzing complexity of {issue_id} for splitting...\n")

        # Example analysis (would analyze actual issue content)
        analysis = {
            "issue_id": issue_id,
            "complexity": "high",
            "estimated_hours": 16,
            "recommended_split": True,
            "suggested_strategy": "acceptance-criteria",
            "suggested_subtasks": [
                {
                    "title": "Implement backend API",
                    "estimate": 4,
                    "description": "Create REST endpoints for feature"
                },
                {
                    "title": "Build frontend UI",
                    "estimate": 4,
                    "description": "Create user interface components"
                },
                {
                    "title": "Add database schema",
                    "estimate": 2,
                    "description": "Design and implement data model"
                },
                {
                    "title": "Write tests",
                    "estimate": 3,
                    "description": "Unit and integration tests"
                },
                {
                    "title": "Documentation",
                    "estimate": 2,
                    "description": "API docs and user guide"
                }
            ]
        }

        self.logger.info(f"Complexity: {analysis['complexity'].upper()}")
        self.logger.info(f"Estimated total time: {analysis['estimated_hours']} hours")
        self.logger.info(f"Recommended split: {'YES' if analysis['recommended_split'] else 'NO'}")
        self.logger.info(f"Suggested strategy: {analysis['suggested_strategy']}\n")

        if analysis['recommended_split']:
            self.logger.info(f"Suggested breakdown into {len(analysis['suggested_subtasks'])} subtasks:\n")
            for i, subtask in enumerate(analysis['suggested_subtasks'], 1):
                self.logger.info(f"{i}. {subtask['title']} ({subtask['estimate']}h)")
                self.logger.info(f"   {subtask['description']}\n")

        return analysis

    def check_critical_path(self, project: str = None) -> List[str]:
        """Identify critical path items."""

        self.logger.info(f"Analyzing critical path{f' for {project}' if project else ''}...\n")

        # Example critical path (would use actual dependency graph)
        critical_path = [
            "ISSUE-101: Database schema design (2h)",
            "ISSUE-102: Backend API implementation (4h)",
            "ISSUE-105: Integration testing (3h)",
            "ISSUE-107: Security audit (4h)",
            "ISSUE-109: Production deployment (2h)"
        ]

        self.logger.info(f"{ICONS['critical_path']} Critical path (items that block other work):\n")
        total_time = 0
        for item in critical_path:
            self.logger.info(f"  → {item}")
            # Extract hours from string (simple parse)
            hours = int(item.split('(')[1].split('h')[0])
            total_time += hours

        self.logger.info(f"\nEstimated critical path duration: {total_time} hours")
        self.logger.info(f"Items that can be parallelized are not shown above.")

        return critical_path

    def auto_escalate(self, threshold_days: int = 3) -> List[Dict]:
        """Find and escalate long-blocked issues."""

        self.logger.info(f"Finding issues blocked for >{threshold_days} days...\n")

        # Example: find stale blocked issues (would use actual API)
        threshold_date = datetime.now() - timedelta(days=threshold_days)
        stale_blocked = [
            {
                "issue_id": "ISSUE-123",
                "blocked_since": (datetime.now() - timedelta(days=5)).isoformat(),
                "blocker": "Waiting for design approval",
                "impact": "high"
            },
            {
                "issue_id": "ISSUE-456",
                "blocked_since": (datetime.now() - timedelta(days=4)).isoformat(),
                "blocker": "Infrastructure not ready",
                "impact": "medium"
            }
        ]

        if not stale_blocked:
            self.logger.success("No issues blocked longer than threshold")
            return []

        self.logger.warning(f"Found {len(stale_blocked)} issue(s) to escalate:\n")
        for issue in stale_blocked:
            blocked_since = datetime.fromisoformat(issue['blocked_since'])
            days = (datetime.now() - blocked_since).days
            self.logger.info(f"  {issue['issue_id']}: blocked {days} days")
            self.logger.info(f"    Blocker: {issue['blocker']}")
            self.logger.info(f"    Impact: {issue['impact'].upper()}")
            self.logger.info(f"    Action: Escalating to managers\n")

        return stale_blocked

    def _find_blockers(self, issue_id: str) -> List[BlockerInfo]:
        """Find direct blockers for an issue."""

        # Example blockers (would query from actual issue)
        blockers = [
            BlockerInfo(
                blocker_id="DESIGN-45",
                description="Waiting for design mockups",
                category="external",
                impact="high",
                blocked_since=datetime.now() - timedelta(days=2),
                eta="End of week",
                suggested_action="Follow up with design team, request ETA update"
            )
        ]
        return blockers

    def _find_transitive_dependencies(self, issue_id: str) -> List[str]:
        """Find transitive (indirect) dependencies."""
        # Example transitive deps
        return [
            "INFRA-101 (needed by DESIGN-45)",
            "API-202 (needed by backend work)",
        ]

    def _calculate_critical_path(self, issue_id: str) -> List[str]:
        """Calculate critical path through dependencies."""
        return [
            "ISSUE-101 (2h) → ISSUE-102 (4h) → Current Issue"
        ]

    def _print_blocker(self, blocker: BlockerInfo):
        """Pretty print blocker information."""
        days_blocked = (datetime.now() - blocker.blocked_since).days

        self.logger.info(f"  {ICONS['blocked']} {blocker.blocker_id}: {blocker.description}")
        self.logger.info(f"     Category: {blocker.category}")
        self.logger.info(f"     Impact: {blocker.impact.upper()}")
        self.logger.info(f"     Blocked for: {days_blocked} days")
        if blocker.eta:
            self.logger.info(f"     ETA: {blocker.eta}")
        self.logger.info("")


def main():
    """Main entry point."""
    logger = Logger()

    parser = argparse.ArgumentParser(description="Analyze blocking issues")
    parser.add_argument("--issue", help="Issue ID to analyze")
    parser.add_argument("--suggest-split", action="store_true", help="Suggest how to split issue")
    parser.add_argument("--critical-path", action="store_true", help="Show critical path")
    parser.add_argument("--project", help="Project name for critical path analysis")
    parser.add_argument("--auto-escalate", action="store_true", help="Auto-escalate stale blocked issues")
    parser.add_argument("--threshold", default="3d", help="Threshold for escalation (e.g., 3d, 1w)")

    args = parser.parse_args()

    analyzer = BlockAnalyzer(logger=logger)

    if args.auto_escalate:
        # Parse threshold (simple version)
        threshold_days = int(args.threshold.rstrip('dw'))
        if args.threshold.endswith('w'):
            threshold_days *= 7

        analyzer.auto_escalate(threshold_days)

    elif args.critical_path:
        analyzer.check_critical_path(args.project)

    elif args.issue:
        if args.suggest_split:
            analyzer.suggest_split(args.issue)
        else:
            analyzer.analyze_issue(args.issue)

    else:
        logger.error("Specify --issue, --critical-path, or --auto-escalate")
        logger.info("Run with --help for usage information")
        sys.exit(1)


if __name__ == "__main__":
    main()
