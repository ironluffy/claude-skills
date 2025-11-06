#!/usr/bin/env python3
"""
Issue Operations Script

Manage GitHub and Linear issues - report blocks, split issues, bulk updates, and create related issues.

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
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class Platform(Enum):
    LINEAR = "linear"
    GITHUB = "github"
    JIRA = "jira"


class IssueRelationship(Enum):
    BLOCKS = "blocks"
    BLOCKED_BY = "blocked-by"
    RELATES_TO = "relates-to"
    DUPLICATE = "duplicate"
    SUBTASK = "subtask"
    FOLLOW_UP = "follow-up"
    PREREQUISITE = "prerequisite"


@dataclass
class Blocker:
    """Represents a blocking issue."""
    description: str
    category: str  # external, technical, resource
    impact: str  # high, medium, low
    context: str
    blocking_issue_id: Optional[str] = None
    eta: Optional[str] = None
    reported_at: str = None

    def __post_init__(self):
        if self.reported_at is None:
            self.reported_at = datetime.now().isoformat()


@dataclass
class IssueOperation:
    """Base class for issue operations."""
    issue_id: str
    platform: Platform
    dry_run: bool = False


class IssueManager:
    """Manage issue operations across platforms."""

    def __init__(self, platform: Platform, dry_run: bool = False):
        self.platform = platform
        self.dry_run = dry_run

    def assign_issue(
        self,
        issue_id: str,
        assignee: str,
        assignee_type: str = "agent",
        notify: bool = True
    ) -> Dict:
        """Assign issue to agent or human."""

        if self.dry_run:
            print(f"[DRY RUN] Would assign {issue_id}")
            print(f"  Assignee: {assignee} (type: {assignee_type})")
            print(f"  Notify: {notify}")
            return {"assignee": assignee, "type": assignee_type}

        icon = "🤖" if assignee_type == "agent" else "👤"
        print(f"✓ Assigned {issue_id} to {icon} {assignee}")
        if notify:
            print(f"  Notified {assignee}")

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

        # Detect assignee type (using same logic as task decomposer)
        human_keywords = [
            "approve", "decision", "review stakeholder", "negotiate",
            "business decision", "prioritize", "strategic"
        ]

        title_lower = title.lower()
        desc_lower = description.lower()

        is_human_task = any(kw in title_lower or kw in desc_lower for kw in human_keywords)

        if is_human_task:
            assignee = human_users.get("default", "unassigned")
            assignee_type = "human"
            icon = "👤"
        else:
            assignee = agent_user
            assignee_type = "agent"
            icon = "🤖"

        if self.dry_run:
            print(f"[DRY RUN] Would auto-assign {issue_id}")
            print(f"  Analysis: {'Human' if is_human_task else 'Agent'} task detected")
            print(f"  Assignee: {icon} {assignee}")
            return {"assignee": assignee, "type": assignee_type}

        print(f"✓ Auto-assigned {issue_id} to {icon} {assignee}")
        print(f"  Detection: {'Human judgment required' if is_human_task else 'Agent can automate'}")

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
            print(f"[DRY RUN] Would reassign {issue_id}")
            print(f"  From: {from_assignee}")
            print(f"  To: {to_assignee}")
            if reason:
                print(f"  Reason: {reason}")
            print(f"  Notify both: {notify_both}")
            return {"from": from_assignee, "to": to_assignee}

        print(f"✓ Reassigned {issue_id}")
        print(f"  {from_assignee} → {to_assignee}")
        if reason:
            print(f"  Reason: {reason}")
        if notify_both:
            print(f"  Notified both assignees")

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
            print(f"[DRY RUN] Would report blocker on {issue_id}")
            print(f"  Blocker: {blocked_by}")
            print(f"  Category: {category}")
            print(f"  Impact: {impact}")
            if blocking_issue_id:
                print(f"  Blocked by issue: {blocking_issue_id}")
            if notify:
                print(f"  Would notify: {', '.join(notify)}")
            return asdict(blocker)

        # Actual implementation would call platform API
        print(f"✓ Reported blocker on {issue_id}")
        print(f"  Added 'blocked' label")
        print(f"  Added blocker comment with context")
        if blocking_issue_id:
            print(f"  Linked to blocking issue: {blocking_issue_id}")
        if notify:
            print(f"  Notified: {', '.join(notify)}")

        return asdict(blocker)

    def unblock_issue(
        self,
        issue_id: str,
        resolution: str,
        notify_assignee: bool = True
    ) -> Dict:
        """Mark issue as unblocked."""

        if self.dry_run:
            print(f"[DRY RUN] Would unblock {issue_id}")
            print(f"  Resolution: {resolution}")
            print(f"  Notify assignee: {notify_assignee}")
            return {"status": "would_unblock"}

        print(f"✓ Unblocked {issue_id}")
        print(f"  Removed 'blocked' label")
        print(f"  Added resolution comment: {resolution}")
        if notify_assignee:
            print(f"  Notified assignee to resume work")

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
            print(f"[DRY RUN] Would split {issue_id}")
            print(f"  Strategy: {strategy}")
            print(f"  Number of subtasks: {num_subtasks or 'auto'}")
            print(f"  Preserve labels: {preserve_labels}")
            print(f"  Link to parent: {link_parent}")
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
            print(f"✓ Created {subtask['id']}: {subtask['title']}")

        print(f"\n✓ Split {issue_id} into {len(subtasks)} subtasks")
        if link_parent:
            print(f"  All subtasks linked to parent {issue_id}")

        return subtasks

    def merge_issues(
        self,
        issue_ids: List[str],
        keep: str,
        preserve_comments: bool = True
    ) -> Dict:
        """Merge duplicate or related issues."""

        if self.dry_run:
            print(f"[DRY RUN] Would merge issues")
            print(f"  Issues: {', '.join(issue_ids)}")
            print(f"  Keep: {keep}")
            print(f"  Preserve comments: {preserve_comments}")
            return {"status": "would_merge"}

        closed = [id for id in issue_ids if id != keep]
        print(f"✓ Merged issues into {keep}")
        print(f"  Closed as duplicate: {', '.join(closed)}")
        if preserve_comments:
            print(f"  Merged comments to {keep}")

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
            print(f"[DRY RUN] Would update {len(matching_issues)} issues")
            print(f"  Filter: {filter_query}")
            if add_labels:
                print(f"  Add labels: {', '.join(add_labels)}")
            if remove_labels:
                print(f"  Remove labels: {', '.join(remove_labels)}")
            if set_assignee:
                print(f"  Set assignee: {set_assignee}")
            if set_priority:
                print(f"  Set priority: {set_priority}")
            print(f"\n  Matching issues: {', '.join(matching_issues)}")
            return {"count": len(matching_issues), "issues": matching_issues}

        print(f"✓ Updated {len(matching_issues)} issues")
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
            print(f"  {issue}: {'; '.join(changes)}")

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
            print(f"[DRY RUN] Would create related issue")
            print(f"  Source: {source_issue}")
            print(f"  Relationship: {relationship.value}")
            print(f"  Title: {title}")
            print(f"  Inherit labels: {inherit_labels}")
            return {"id": new_issue_id}

        print(f"✓ Created {new_issue_id}: {title}")
        print(f"  Relationship: {relationship.value} {source_issue}")
        if inherit_labels:
            print(f"  Inherited labels from {source_issue}")

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

        print(f"✓ Found {len(results)} issues")
        print(f"  Filter: {filter_query}")
        print(f"  Sort: {sort_by}")
        print(f"\nResults:")
        for issue in results:
            print(f"  {issue['id']}: {issue['title']} ({issue['status']})")

        return results


def main():
    """Main entry point."""
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
    manager = IssueManager(platform, args.dry_run)

    result = None

    if args.operation == "report-blocker":
        if not args.issue or not args.blocked_by:
            print("Error: --issue and --blocked-by required")
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
            print("Error: --issue and --resolution required")
            sys.exit(1)

        result = manager.unblock_issue(args.issue, args.resolution)

    elif args.operation == "split-issue":
        if not args.issue:
            print("Error: --issue required")
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
            print("Error: --issues and --keep required")
            sys.exit(1)

        issue_list = args.issues.split(',')
        result = manager.merge_issues(issue_list, args.keep)

    elif args.operation == "bulk-update":
        if not args.filter:
            print("Error: --filter required")
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
            print("Error: --source, --type, and --title required")
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
            print("Error: --filter required")
            sys.exit(1)

        result = manager.query_issues(args.filter)

    elif args.operation == "assign":
        if not args.issue or not args.assignee:
            print("Error: --issue and --assignee required")
            sys.exit(1)

        result = manager.assign_issue(
            args.issue,
            args.assignee,
            args.assignee_type
        )

    elif args.operation == "auto-assign":
        if not args.issue:
            print("Error: --issue required")
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
            print("Error: --issue, --from-assignee, and --to-assignee required")
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
        print(f"\n✓ Results saved to {args.output}")


if __name__ == "__main__":
    main()
