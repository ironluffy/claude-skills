#!/usr/bin/env python3
"""
Issue Operations Script

Manage GitHub and Linear issues - report blocks, split issues, bulk updates, and create related issues.

Refactored to use professional logging and centralized constants.

Usage:
    python issue_operations.py <operation> [options]

Operations:
    report-blocker    Report what's blocking an issue
    unblock           Mark issue as unblocked
    split-issue       Break large issue into smaller pieces
    merge-issues      Combine duplicate issues
    bulk-update       Update multiple issues
    create-related    Create linked related issue
    query             Find issues matching criteria

Examples:
    python issue_operations.py report-blocker --issue ISSUE-123 --blocked-by "API design"
    python issue_operations.py split-issue --issue ISSUE-456 --num-subtasks 4
    python issue_operations.py bulk-update --filter "label:backend" --add-label "needs-review"
    python issue_operations.py create-related --source ISSUE-789 --type follow-up --title "Tests"
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import asdict
from datetime import datetime

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from logger import Logger

# Import constants
from constants import (
    Platform,
    IssueRelationship,
    Blocker,
    HUMAN_KEYWORDS,
    AGENT_KEYWORDS,
    DRY_RUN_PREFIX,
    ICONS,
    ERROR_MESSAGES,
    DEFAULT_QUERY_LIMIT,
    DEFAULT_SORT_ORDER
)


class IssueManager:
    """Manage issue operations across platforms."""

    def __init__(self, platform: Platform, dry_run: bool = False, logger: Logger = None):
        """Initialize issue manager with platform and dry-run mode."""
        self.platform = platform
        self.dry_run = dry_run
        self.logger = logger or Logger()

    def assign_issue(
        self,
        issue_id: str,
        assignee: str,
        assignee_type: str = "agent",
        notify: bool = True
    ) -> Dict:
        """Assign issue to agent or human."""

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would assign {issue_id}")
            self.logger.info(f"  Assignee: {assignee} (type: {assignee_type})")
            self.logger.info(f"  Notify: {notify}")
            return {"assignee": assignee, "type": assignee_type}

        icon = ICONS["agent"] if assignee_type == "agent" else ICONS["human"]
        self.logger.success(f"Assigned {issue_id} to {icon} {assignee}")
        if notify:
            self.logger.info(f"  Notified {assignee}")

        return {"issue": issue_id, "assignee": assignee, "type": assignee_type}

    def auto_assign(
        self,
        issue_id: str,
        agent_user: str = "agent",
        human_users: Dict[str, str] = None
    ) -> Dict:
        """
        Auto-assign issue based on content analysis.

        Detects whether task requires agent or human intervention.
        """
        human_users = human_users or {}

        # In production, this would fetch issue details from API
        # For now, use placeholder logic
        title = f"Issue {issue_id}"
        description = "Sample issue description"
        labels = ["development"]

        # Detect assignee type (using keywords from constants)
        title_lower = title.lower()
        desc_lower = description.lower()

        is_human_task = any(kw in title_lower or kw in desc_lower for kw in HUMAN_KEYWORDS)

        if is_human_task:
            assignee = human_users.get("default", "unassigned")
            assignee_type = "human"
            icon = ICONS["human"]
        else:
            assignee = agent_user
            assignee_type = "agent"
            icon = ICONS["agent"]

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would auto-assign {issue_id}")
            self.logger.info(f"  Analysis: {'Human' if is_human_task else 'Agent'} task detected")
            self.logger.info(f"  Assignee: {icon} {assignee}")
            return {"assignee": assignee, "type": assignee_type}

        self.logger.success(f"Auto-assigned {issue_id} to {icon} {assignee}")
        self.logger.info(f"  Detection: {'Human judgment required' if is_human_task else 'Agent can automate'}")

        return {
            "issue": issue_id,
            "assignee": assignee,
            "type": assignee_type,
            "auto_detected": True
        }

    def reassign_issue(
        self,
        issue_id: str,
        from_assignee: str,
        to_assignee: str,
        reason: str = "",
        notify_both: bool = True
    ) -> Dict:
        """Reassign issue from one assignee to another."""

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would reassign {issue_id}")
            self.logger.info(f"  From: {from_assignee}")
            self.logger.info(f"  To: {to_assignee}")
            if reason:
                self.logger.info(f"  Reason: {reason}")
            self.logger.info(f"  Notify both: {notify_both}")
            return {"from": from_assignee, "to": to_assignee}

        self.logger.success(f"Reassigned {issue_id}")
        self.logger.info(f"  {from_assignee} → {to_assignee}")
        if reason:
            self.logger.info(f"  Reason: {reason}")
        if notify_both:
            self.logger.info(f"  Notified both assignees")

        return {
            "issue": issue_id,
            "from": from_assignee,
            "to": to_assignee,
            "reason": reason
        }

    def report_blocker(
        self,
        issue_id: str,
        blocked_by: str,
        category: str = "external",
        impact: str = "medium",
        context: str = "",
        blocking_issue_id: str = None,
        notify: List[str] = None
    ) -> Dict:
        """Report what's blocking an issue."""

        blocker = Blocker(
            description=blocked_by,
            category=category,
            impact=impact,
            context=context,
            blocking_issue_id=blocking_issue_id
        )

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would report blocker on {issue_id}")
            self.logger.info(f"  Blocker: {blocked_by}")
            self.logger.info(f"  Category: {category}")
            self.logger.info(f"  Impact: {impact}")
            if blocking_issue_id:
                self.logger.info(f"  Blocked by issue: {blocking_issue_id}")
            if notify:
                self.logger.info(f"  Would notify: {', '.join(notify)}")
            return asdict(blocker)

        # Actual implementation would call platform API
        self.logger.success(f"Reported blocker on {issue_id}")
        self.logger.info(f"  Added 'blocked' label")
        self.logger.info(f"  Added blocker comment with context")
        if blocking_issue_id:
            self.logger.info(f"  Linked to blocking issue: {blocking_issue_id}")
        if notify:
            self.logger.info(f"  Notified: {', '.join(notify)}")

        return asdict(blocker)

    def unblock_issue(
        self,
        issue_id: str,
        resolution: str,
        notify_assignee: bool = True
    ) -> Dict:
        """Mark issue as unblocked."""

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would unblock {issue_id}")
            self.logger.info(f"  Resolution: {resolution}")
            self.logger.info(f"  Notify assignee: {notify_assignee}")
            return {"status": "would_unblock"}

        self.logger.success(f"Unblocked {issue_id}")
        self.logger.info(f"  Removed 'blocked' label")
        self.logger.info(f"  Added resolution comment: {resolution}")
        if notify_assignee:
            self.logger.info(f"  Notified assignee to resume work")

        return {"status": "unblocked", "resolution": resolution}

    def split_issue(
        self,
        issue_id: str,
        num_subtasks: int = None,
        strategy: str = "acceptance-criteria",
        preserve_labels: bool = True,
        link_parent: bool = True
    ) -> List[Dict]:
        """Split large issue into smaller subtasks."""

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would split {issue_id}")
            self.logger.info(f"  Strategy: {strategy}")
            self.logger.info(f"  Number of subtasks: {num_subtasks or 'auto'}")
            self.logger.info(f"  Preserve labels: {preserve_labels}")
            self.logger.info(f"  Link to parent: {link_parent}")
            return []

        # Example split (actual implementation would analyze issue content)
        subtasks = []
        for i in range(num_subtasks or 3):
            subtask = {
                "id": f"{issue_id}-{i+1}",
                "title": f"Subtask {i+1} from {issue_id}",
                "parent": issue_id if link_parent else None,
                "labels": ["inherited"] if preserve_labels else []
            }
            subtasks.append(subtask)
            self.logger.success(f"Created {subtask['id']}: {subtask['title']}")

        self.logger.success(f"\nSplit {issue_id} into {len(subtasks)} subtasks")
        if link_parent:
            self.logger.info(f"  All subtasks linked to parent {issue_id}")

        return subtasks

    def merge_issues(
        self,
        issue_ids: List[str],
        keep: str,
        preserve_comments: bool = True
    ) -> Dict:
        """Merge duplicate or related issues."""

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would merge issues")
            self.logger.info(f"  Issues: {', '.join(issue_ids)}")
            self.logger.info(f"  Keep: {keep}")
            self.logger.info(f"  Preserve comments: {preserve_comments}")
            return {"status": "would_merge"}

        closed = [id for id in issue_ids if id != keep]
        self.logger.success(f"Merged issues into {keep}")
        self.logger.info(f"  Closed as duplicate: {', '.join(closed)}")
        if preserve_comments:
            self.logger.info(f"  Merged comments to {keep}")

        return {"primary": keep, "merged": closed}

    def bulk_update(
        self,
        filter_query: str,
        add_labels: List[str] = None,
        remove_labels: List[str] = None,
        set_assignee: str = None,
        set_priority: str = None,
        add_comment: str = None
    ) -> Dict:
        """Update multiple issues matching criteria."""

        # Example: find matching issues (would use actual API)
        matching_issues = [f"ISSUE-{i}" for i in range(1, 6)]

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would update {len(matching_issues)} issues")
            self.logger.info(f"  Filter: {filter_query}")
            if add_labels:
                self.logger.info(f"  Add labels: {', '.join(add_labels)}")
            if remove_labels:
                self.logger.info(f"  Remove labels: {', '.join(remove_labels)}")
            if set_assignee:
                self.logger.info(f"  Set assignee: {set_assignee}")
            if set_priority:
                self.logger.info(f"  Set priority: {set_priority}")
            self.logger.info(f"\n  Matching issues: {', '.join(matching_issues)}")
            return {"count": len(matching_issues), "issues": matching_issues}

        self.logger.success(f"Updated {len(matching_issues)} issues")
        for issue in matching_issues:
            changes = []
            if add_labels:
                changes.append(f"added labels: {', '.join(add_labels)}")
            if remove_labels:
                changes.append(f"removed labels: {', '.join(remove_labels)}")
            if set_assignee:
                changes.append(f"assigned to {set_assignee}")
            if set_priority:
                changes.append(f"priority → {set_priority}")
            self.logger.info(f"  {issue}: {'; '.join(changes)}")

        return {"count": len(matching_issues), "updated": matching_issues}

    def create_related(
        self,
        source_issue: str,
        relationship: IssueRelationship,
        title: str,
        description: str = "",
        inherit_labels: bool = False
    ) -> Dict:
        """Create related issue linked to source."""

        new_issue_id = f"NEW-{hash(title) % 1000}"

        if self.dry_run:
            self.logger.info(f"{DRY_RUN_PREFIX} Would create related issue")
            self.logger.info(f"  Source: {source_issue}")
            self.logger.info(f"  Relationship: {relationship.value}")
            self.logger.info(f"  Title: {title}")
            self.logger.info(f"  Inherit labels: {inherit_labels}")
            return {"id": new_issue_id}

        self.logger.success(f"Created {new_issue_id}: {title}")
        self.logger.info(f"  Relationship: {relationship.value} {source_issue}")
        if inherit_labels:
            self.logger.info(f"  Inherited labels from {source_issue}")

        return {
            "id": new_issue_id,
            "title": title,
            "source": source_issue,
            "relationship": relationship.value
        }

    def query_issues(
        self,
        filter_query: str,
        sort_by: str = "updated:desc",
        limit: int = 50
    ) -> List[Dict]:
        """Query issues matching criteria."""

        # Example results (would use actual API)
        results = [
            {"id": f"ISSUE-{i}", "title": f"Issue {i}", "status": "open"}
            for i in range(1, min(6, limit + 1))
        ]

        self.logger.success(f"Found {len(results)} issues")
        self.logger.info(f"  Filter: {filter_query}")
        self.logger.info(f"  Sort: {sort_by}")
        self.logger.info(f"\nResults:")
        for issue in results:
            self.logger.info(f"  {issue['id']}: {issue['title']} ({issue['status']})")

        return results


def main():
    """Main entry point."""
    logger = Logger()

    parser = argparse.ArgumentParser(description="Manage GitHub and Linear issues with intelligent agent/human assignment")
    parser.add_argument("operation", choices=[
        "report-blocker", "unblock", "split-issue", "merge-issues",
        "bulk-update", "create-related", "query",
        "assign", "auto-assign", "reassign"
    ])
    parser.add_argument("--platform", choices=["linear", "github", "jira"], default="linear")
    parser.add_argument("--issue", help="Issue ID")
    parser.add_argument("--blocked-by", help="What's blocking")
    parser.add_argument("--category", choices=["external", "technical", "resource"], default="external")
    parser.add_argument("--impact", choices=["high", "medium", "low"], default="medium")
    parser.add_argument("--context", help="Additional context")
    parser.add_argument("--blocking-issue", help="ID of blocking issue")
    parser.add_argument("--resolution", help="How blocker was resolved")
    parser.add_argument("--num-subtasks", type=int, help="Number of subtasks to create")
    parser.add_argument("--strategy", choices=["acceptance-criteria", "functionality", "layer"], default="acceptance-criteria")
    parser.add_argument("--issues", help="Comma-separated issue IDs")
    parser.add_argument("--keep", help="Issue to keep when merging")
    parser.add_argument("--filter", help="Query filter")
    parser.add_argument("--add-label", action="append", help="Label to add")
    parser.add_argument("--remove-label", action="append", help="Label to remove")
    parser.add_argument("--set-assignee", help="Assignee to set")
    parser.add_argument("--set-priority", help="Priority to set")
    parser.add_argument("--comment", help="Comment to add")
    parser.add_argument("--source", help="Source issue for related issue")
    parser.add_argument("--assignee", help="User/agent to assign to")
    parser.add_argument("--assignee-type", choices=["agent", "human"], default="agent", help="Type of assignee")
    parser.add_argument("--agent-user", default="agent", help="User ID for agent assignments")
    parser.add_argument("--human-users", help="Comma-separated role:user_id pairs")
    parser.add_argument("--from-assignee", help="Current assignee (for reassignment)")
    parser.add_argument("--to-assignee", help="New assignee (for reassignment)")
    parser.add_argument("--reason", help="Reason for reassignment")
    parser.add_argument("--type", choices=["follow-up", "prerequisite", "related", "subtask"], help="Relationship type")
    parser.add_argument("--title", help="Title for new issue")
    parser.add_argument("--description", help="Description for new issue")
    parser.add_argument("--notify", help="Users to notify (comma-separated)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without executing")
    parser.add_argument("--preserve-labels", action="store_true", help="Preserve labels when splitting")
    parser.add_argument("--inherit-labels", action="store_true", help="Inherit labels from source")
    parser.add_argument("--link-parent", action="store_true", default=True, help="Link to parent issue")
    parser.add_argument("--output", help="Output file for results")

    args = parser.parse_args()

    platform = Platform(args.platform)
    manager = IssueManager(platform, args.dry_run, logger=logger)

    result = None

    if args.operation == "report-blocker":
        if not args.issue or not args.blocked_by:
            logger.error(ERROR_MESSAGES["missing_blocker"])
            sys.exit(1)

        notify = args.notify.split(',') if args.notify else None
        result = manager.report_blocker(
            args.issue,
            args.blocked_by,
            args.category,
            args.impact,
            args.context or "",
            args.blocking_issue,
            notify
        )

    elif args.operation == "unblock":
        if not args.issue or not args.resolution:
            logger.error(ERROR_MESSAGES["missing_resolution"])
            sys.exit(1)

        result = manager.unblock_issue(args.issue, args.resolution)

    elif args.operation == "split-issue":
        if not args.issue:
            logger.error(ERROR_MESSAGES["missing_issue"])
            sys.exit(1)

        result = manager.split_issue(
            args.issue,
            args.num_subtasks,
            args.strategy,
            args.preserve_labels,
            args.link_parent
        )

    elif args.operation == "merge-issues":
        if not args.issues or not args.keep:
            logger.error(ERROR_MESSAGES["missing_merge"])
            sys.exit(1)

        issue_list = args.issues.split(',')
        result = manager.merge_issues(issue_list, args.keep)

    elif args.operation == "bulk-update":
        if not args.filter:
            logger.error(ERROR_MESSAGES["missing_filter"])
            sys.exit(1)

        result = manager.bulk_update(
            args.filter,
            args.add_label,
            args.remove_label,
            args.set_assignee,
            args.set_priority,
            args.comment
        )

    elif args.operation == "create-related":
        if not args.source or not args.type or not args.title:
            logger.error(ERROR_MESSAGES["missing_source"])
            sys.exit(1)

        relationship_map = {
            "follow-up": IssueRelationship.FOLLOW_UP,
            "prerequisite": IssueRelationship.PREREQUISITE,
            "related": IssueRelationship.RELATES_TO,
            "subtask": IssueRelationship.SUBTASK
        }

        result = manager.create_related(
            args.source,
            relationship_map[args.type],
            args.title,
            args.description or "",
            args.inherit_labels
        )

    elif args.operation == "query":
        if not args.filter:
            logger.error(ERROR_MESSAGES["missing_filter"])
            sys.exit(1)

        result = manager.query_issues(args.filter)

    elif args.operation == "assign":
        if not args.issue or not args.assignee:
            logger.error(ERROR_MESSAGES["missing_assignee"])
            sys.exit(1)

        result = manager.assign_issue(
            args.issue,
            args.assignee,
            args.assignee_type
        )

    elif args.operation == "auto-assign":
        if not args.issue:
            logger.error(ERROR_MESSAGES["missing_issue"])
            sys.exit(1)

        # Parse human users mapping
        human_users = {}
        if args.human_users:
            for pair in args.human_users.split(','):
                if ':' in pair:
                    role, user_id = pair.split(':', 1)
                    human_users[role.strip()] = user_id.strip()

        result = manager.auto_assign(
            args.issue,
            args.agent_user,
            human_users
        )

    elif args.operation == "reassign":
        if not args.issue or not args.from_assignee or not args.to_assignee:
            logger.error(ERROR_MESSAGES["missing_reassign"])
            sys.exit(1)

        result = manager.reassign_issue(
            args.issue,
            args.from_assignee,
            args.to_assignee,
            args.reason or ""
        )

    # Save output if requested
    if args.output and result:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        logger.success(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
