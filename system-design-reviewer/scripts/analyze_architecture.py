#!/usr/bin/env python3
"""
Architecture Analyzer - Check architecture best practices
"""

import os
import re
from pathlib import Path


class ArchitectureAnalyzer:
    """Analyze architecture patterns and best practices"""

    def __init__(self, project_path):
        self.project_path = Path(project_path)

    def analyze(self):
        """Run architecture analysis"""
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

        return results

    def _find_strengths(self):
        """Identify architecture strengths"""
        strengths = []

        # Check for separation of concerns
        has_dirs = {
            "controllers": any(self.project_path.rglob("*controller*")),
            "models": any(self.project_path.rglob("*model*")),
            "services": any(self.project_path.rglob("*service*")),
            "tests": any(self.project_path.rglob("test*"))
        }

        if has_dirs["controllers"] and has_dirs["models"]:
            strengths.append("Well-separated components (MVC pattern)")

        if has_dirs["tests"]:
            strengths.append("Test infrastructure in place")

        # Check for configuration management
        if any(self.project_path.rglob("*.env.example")):
            strengths.append("Environment configuration template provided")

        # Check for Docker
        if any(self.project_path.rglob("Dockerfile")):
            strengths.append("Containerized application (Docker)")

        return strengths or ["Project structure is organized"]

    def _find_issues(self):
        """Find architecture issues"""
        high_issues = []
        medium_issues = []
        low_issues = []

        # Check for single database instance
        if not self._has_db_replication():
            high_issues.append({
                "title": "No database replication detected",
                "impact": "Single point of failure for data storage",
                "recommendation": "Implement database replication (primary + replicas)",
                "effort": "4 hours",
                "cost_impact": "+$50/month"
            })

        # Check for caching
        if not self._has_caching():
            medium_issues.append({
                "title": "No caching layer detected",
                "impact": "High database load, slower response times",
                "recommendation": "Add Redis or Memcached caching",
                "effort": "6 hours",
                "cost_impact": "+$30/month"
            })

        # Check for load balancing
        if not self._has_load_balancer():
            medium_issues.append({
                "title": "No load balancer configuration",
                "impact": "Cannot horizontally scale",
                "recommendation": "Add load balancer (nginx/HAProxy/ALB)",
                "effort": "3 hours",
                "cost_impact": "+$20/month"
            })

        # Check for health checks
        if not self._has_health_checks():
            low_issues.append({
                "title": "No health check endpoints",
                "impact": "Difficult to monitor service status",
                "recommendation": "Add /health and /ready endpoints",
                "effort": "1 hour",
                "cost_impact": "None"
            })

        return high_issues, medium_issues, low_issues

    def _has_db_replication(self):
        """Check for database replication config"""
        patterns = ["replica", "replication", "read_replica", "slave"]
        for config_file in self.project_path.rglob("*.{yml,yaml,json,conf}"):
            try:
                content = config_file.read_text().lower()
                if any(pattern in content for pattern in patterns):
                    return True
            except Exception:
                continue
        return False

    def _has_caching(self):
        """Check for caching implementation"""
        cache_indicators = ["redis", "memcache", "cache"]
        for file in self.project_path.rglob("*"):
            if file.is_file():
                try:
                    if any(indicator in file.name.lower() for indicator in cache_indicators):
                        return True
                    if file.suffix in ['.py', '.js', '.java', '.go']:
                        content = file.read_text().lower()
                        if any(f"import {indicator}" in content or f"require('{indicator}" in content
                               for indicator in cache_indicators):
                            return True
                except Exception:
                    continue
        return False

    def _has_load_balancer(self):
        """Check for load balancer config"""
        lb_files = ["nginx.conf", "haproxy.cfg", "load-balancer.yml"]
        return any(self.project_path.rglob(pattern) for pattern in lb_files)

    def _has_health_checks(self):
        """Check for health check endpoints"""
        for code_file in self.project_path.rglob("*"):
            if code_file.suffix in ['.py', '.js', '.java', '.go', '.rb']:
                try:
                    content = code_file.read_text()
                    if re.search(r'[\'"/]health[\'":]|[\'"/]ready[\'":]', content, re.IGNORECASE):
                        return True
                except Exception:
                    continue
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
