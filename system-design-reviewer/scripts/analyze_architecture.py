#!/usr/bin/env python3
"""
Architecture Analyzer - Check architecture best practices
Part of system-design-reviewer skill for Claude Skills

Refactored to use BaseAnalyzer and shared utilities.
"""

import re
from pathlib import Path

from analyzer_base import BaseAnalyzer
from constants import (
    ARCHITECTURE_INDICATORS,
    MVC_DIRECTORIES,
    CODE_EXTENSIONS,
    CONFIG_EXTENSIONS
)


class ArchitectureAnalyzer(BaseAnalyzer):
    """Analyze architecture patterns and best practices"""

    def analyze(self):
        """Run architecture analysis"""
        self._log_analysis_start("Architecture")

        results = {
            "issue_count": 0,
            "recommendation_count": 0,
            "strengths": [],
            "high_issues": [],
            "medium_issues": [],
            "low_issues": []
        }

        # Check for common patterns
        results["strengths"] = self._find_strengths()

        # Check for issues
        high, medium, low = self._find_issues()
        results["high_issues"] = high
        results["medium_issues"] = medium
        results["low_issues"] = low

        results["issue_count"] = len(high) + len(medium) + len(low)
        results["recommendation_count"] = results["issue_count"]

        self._log_analysis_complete(results)

        return results

    def _find_strengths(self):
        """Identify architecture strengths"""
        strengths = []

        # Check for separation of concerns
        has_dirs = self._check_directory_exists(MVC_DIRECTORIES)

        if has_dirs.get("controllers") and has_dirs.get("models"):
            strengths.append("Well-separated components (MVC pattern)")

        if has_dirs.get("tests"):
            strengths.append("Test infrastructure in place")

        # Check for configuration management
        if self._find_files_by_pattern("*.env.example"):
            strengths.append("Environment configuration template provided")

        # Check for Docker
        if self._find_files_by_pattern("Dockerfile"):
            strengths.append("Containerized application (Docker)")

        return strengths or ["Project structure is organized"]

    def _find_issues(self):
        """Find architecture issues"""
        high_issues = []
        medium_issues = []
        low_issues = []

        # Check for single database instance
        if not self._has_db_replication():
            high_issues.append(self._create_issue(
                title="No database replication detected",
                impact="Single point of failure for data storage",
                recommendation="Implement database replication (primary + replicas)",
                effort="4 hours",
                cost_impact="+$50/month"
            ))

        # Check for caching
        if not self._has_caching():
            medium_issues.append(self._create_issue(
                title="No caching layer detected",
                impact="High database load, slower response times",
                recommendation="Add Redis or Memcached caching",
                effort="6 hours",
                cost_impact="+$30/month"
            ))

        # Check for load balancing
        if not self._has_load_balancer():
            medium_issues.append(self._create_issue(
                title="No load balancer configuration",
                impact="Cannot horizontally scale",
                recommendation="Add load balancer (nginx/HAProxy/ALB)",
                effort="3 hours",
                cost_impact="+$20/month"
            ))

        # Check for health checks
        if not self._has_health_checks():
            low_issues.append(self._create_issue(
                title="No health check endpoints",
                impact="Difficult to monitor service status",
                recommendation="Add /health and /ready endpoints",
                effort="1 hour",
                cost_impact="None"
            ))

        return high_issues, medium_issues, low_issues

    def _has_db_replication(self):
        """Check for database replication config"""
        return self._contains_technology(
            ARCHITECTURE_INDICATORS['database_replication'],
            CONFIG_EXTENSIONS
        )

    def _has_caching(self):
        """Check for caching implementation"""
        return self._contains_technology(
            ARCHITECTURE_INDICATORS['caching'],
            CODE_EXTENSIONS + CONFIG_EXTENSIONS
        )

    def _has_load_balancer(self):
        """Check for load balancer config"""
        lb_files = ARCHITECTURE_INDICATORS['load_balancer']
        for pattern in lb_files:
            if self._find_files_by_pattern(pattern):
                return True
        return False

    def _has_health_checks(self):
        """Check for health check endpoints"""
        code_files = self._get_code_files()

        for code_file in code_files:
            content = self._read_file_safe(code_file)
            if content and re.search(r'[\'"/]health[\'":]|[\'"/]ready[\'":]', content, re.IGNORECASE):
                return True

        return False


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 analyze_architecture.py <project_path>")
        sys.exit(1)

    analyzer = ArchitectureAnalyzer(sys.argv[1])
    results = analyzer.analyze()
    print(json.dumps(results, indent=2))
