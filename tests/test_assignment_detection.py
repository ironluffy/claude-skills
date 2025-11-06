#!/usr/bin/env python3
"""
Tests for intelligent assignment detection logic.

Run with: python -m pytest tests/test_assignment_detection.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'task-decomposer', 'scripts'))

from analyze_task import detect_assignee_type, AssigneeType


class TestAgentDetection:
    """Test detection of agent-suitable tasks."""

    def test_implement_keyword(self):
        """Should detect 'implement' as agent task."""
        assignee_type, needs_review = detect_assignee_type(
            "Implement user authentication",
            "Build authentication system",
            ["backend"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert not needs_review

    def test_refactor_keyword(self):
        """Should detect 'refactor' as agent task."""
        assignee_type, needs_review = detect_assignee_type(
            "Refactor payment processing code",
            "Clean up legacy code",
            ["refactoring"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert not needs_review

    def test_write_test_keyword(self):
        """Should detect 'write test' as agent task."""
        assignee_type, needs_review = detect_assignee_type(
            "Write unit tests for API",
            "Create comprehensive test coverage",
            ["testing"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert not needs_review

    def test_build_keyword(self):
        """Should detect 'build' as agent task."""
        assignee_type, needs_review = detect_assignee_type(
            "Build REST API endpoints",
            "Develop new API functionality",
            ["api", "backend"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert not needs_review


class TestHumanDetection:
    """Test detection of human-required tasks."""

    def test_approve_keyword(self):
        """Should detect 'approve' as human task."""
        assignee_type, needs_review = detect_assignee_type(
            "Approve production deployment",
            "Final sign-off required",
            ["approval"]
        )
        assert assignee_type == AssigneeType.HUMAN
        assert not needs_review

    def test_decision_keyword(self):
        """Should detect 'decision' as human task."""
        assignee_type, needs_review = detect_assignee_type(
            "Make architecture decision",
            "Decision needed on database choice",
            ["planning"]
        )
        assert assignee_type == AssigneeType.HUMAN
        assert not needs_review

    def test_negotiate_keyword(self):
        """Should detect 'negotiate' as human task."""
        assignee_type, needs_review = detect_assignee_type(
            "Negotiate with vendor",
            "Work out pricing and contract terms",
            ["business"]
        )
        assert assignee_type == AssigneeType.HUMAN
        assert not needs_review

    def test_stakeholder_keyword(self):
        """Should detect 'stakeholder' as human task."""
        assignee_type, needs_review = detect_assignee_type(
            "Review with stakeholders",
            "Get stakeholder feedback",
            ["review"]
        )
        assert assignee_type == AssigneeType.HUMAN
        assert not needs_review


class TestReviewRequired:
    """Test detection of tasks requiring human review."""

    def test_security_implementation(self):
        """Should detect security implementation needs review."""
        assignee_type, needs_review = detect_assignee_type(
            "Implement security audit logging",
            "Build audit trail for security events",
            ["security", "backend"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert needs_review

    def test_authentication_implementation(self):
        """Should detect authentication needs review."""
        assignee_type, needs_review = detect_assignee_type(
            "Implement JWT authentication",
            "Build authentication system with JWT",
            ["backend", "authentication"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert needs_review

    def test_payment_implementation(self):
        """Should detect payment processing needs review."""
        assignee_type, needs_review = detect_assignee_type(
            "Implement Stripe payment processing",
            "Build payment integration",
            ["backend", "payment"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert needs_review

    def test_security_audit_human(self):
        """Should detect security audit as human task."""
        assignee_type, needs_review = detect_assignee_type(
            "Conduct security audit",
            "Review security vulnerabilities",
            ["security", "audit"]
        )
        assert assignee_type == AssigneeType.HUMAN
        assert not needs_review


class TestEdgeCases:
    """Test edge cases and mixed signals."""

    def test_mixed_implementation_and_approval(self):
        """Mixed signals should prioritize human."""
        assignee_type, needs_review = detect_assignee_type(
            "Implement feature and get approval",
            "Build feature then approve deployment",
            ["backend"]
        )
        # 'approve' should win over 'implement'
        assert assignee_type == AssigneeType.HUMAN

    def test_empty_labels(self):
        """Should handle empty labels."""
        assignee_type, needs_review = detect_assignee_type(
            "Implement caching",
            "Add Redis caching",
            []
        )
        assert assignee_type == AssigneeType.AGENT
        assert not needs_review

    def test_only_labels(self):
        """Should detect from labels when title/description neutral."""
        assignee_type, needs_review = detect_assignee_type(
            "Task XYZ",
            "Do the thing",
            ["security"]
        )
        # Security label should trigger review requirement
        assert needs_review

    def test_planning_label(self):
        """Planning label should allow either."""
        assignee_type, needs_review = detect_assignee_type(
            "Plan database schema",
            "Design the schema",
            ["planning"]
        )
        assert assignee_type == AssigneeType.EITHER
        assert not needs_review

    def test_no_keywords(self):
        """Default should be agent when no clear signals."""
        assignee_type, needs_review = detect_assignee_type(
            "Update configuration",
            "Change config file",
            ["config"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert not needs_review


class TestCaseSensitivity:
    """Test that detection is case-insensitive."""

    def test_uppercase_implement(self):
        """Should detect IMPLEMENT."""
        assignee_type, needs_review = detect_assignee_type(
            "IMPLEMENT feature",
            "BUILD the thing",
            []
        )
        assert assignee_type == AssigneeType.AGENT

    def test_mixed_case_approve(self):
        """Should detect ApPrOvE."""
        assignee_type, needs_review = detect_assignee_type(
            "ApPrOvE the deployment",
            "Get sign off",
            []
        )
        assert assignee_type == AssigneeType.HUMAN


class TestRealWorldExamples:
    """Test real-world task examples."""

    def test_database_migration(self):
        """Database migration should need review."""
        assignee_type, needs_review = detect_assignee_type(
            "Run production database migration",
            "Execute migration scripts in production",
            ["database", "migration"]
        )
        # Migration keyword should trigger review
        assert needs_review

    def test_unit_tests(self):
        """Writing tests should be pure agent work."""
        assignee_type, needs_review = detect_assignee_type(
            "Write unit tests for UserService",
            "Create comprehensive test suite with 90% coverage",
            ["testing"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert not needs_review

    def test_legal_review(self):
        """Legal work is human-only."""
        assignee_type, needs_review = detect_assignee_type(
            "Legal compliance review",
            "Review for GDPR compliance",
            ["legal", "compliance"]
        )
        assert assignee_type == AssigneeType.HUMAN
        assert not needs_review

    def test_api_documentation(self):
        """API docs generation is agent work."""
        assignee_type, needs_review = detect_assignee_type(
            "Generate API documentation",
            "Auto-generate OpenAPI spec from code",
            ["documentation"]
        )
        assert assignee_type == AssigneeType.AGENT
        assert not needs_review

    def test_ux_decision(self):
        """UX decisions are human work."""
        assignee_type, needs_review = detect_assignee_type(
            "Make UX decision on checkout flow",
            "Decide between one-page vs multi-step checkout",
            ["ux", "design"]
        )
        assert assignee_type == AssigneeType.HUMAN
        assert not needs_review


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
