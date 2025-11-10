#!/usr/bin/env python3
"""
Performance Analyzer - Identify performance bottlenecks and optimization opportunities
Part of system-design-reviewer skill for Claude Skills

Refactored to use BaseAnalyzer and shared utilities.
"""

import re
from pathlib import Path

from analyzer_base import BaseAnalyzer
from constants import (
    PERFORMANCE_INDICATORS,
    N_PLUS_ONE_PATTERNS,
    CODE_EXTENSIONS
)


class PerformanceAnalyzer(BaseAnalyzer):
    """Analyze performance bottlenecks"""

    def analyze(self):
        """Run performance analysis"""
        self._log_analysis_start("Performance")

        results = {
            "optimization_count": 0,
            "strengths": [],
            "high_impact": [],
            "medium_impact": [],
            "low_impact": []
        }

        # Find strengths
        results["strengths"] = self._find_strengths()

        # Find optimization opportunities
        high, medium, low = self._find_optimizations()
        results["high_impact"] = high
        results["medium_impact"] = medium
        results["low_impact"] = low

        results["optimization_count"] = len(high) + len(medium) + len(low)

        self._log_analysis_complete(results)

        return results

    def _find_strengths(self):
        """Find performance strengths"""
        strengths = []

        if self._has_caching():
            strengths.append("Caching implementation detected")

        if self._has_connection_pooling():
            strengths.append("Database connection pooling configured")

        if self._has_async_processing():
            strengths.append("Async processing for background tasks")

        if self._has_indexes():
            strengths.append("Database indexes detected")

        return strengths or ["Basic performance patterns in place"]

    def _find_optimizations(self):
        """Find performance optimization opportunities"""
        high_impact = []
        medium_impact = []
        low_impact = []

        # Check for caching opportunities
        if not self._has_caching():
            high_impact.append({
                "title": "Add Redis caching layer",
                "current": "Direct database queries for all requests",
                "expected": "10x faster response time with caching",
                "implementation": "6 hours",
                "cost": "+$30/month"
            })

        # Check for N+1 queries
        if self._has_n_plus_one_queries():
            high_impact.append({
                "title": "Fix N+1 query problems",
                "current": "Multiple queries per request",
                "expected": "3-5x faster with eager loading",
                "implementation": "4 hours",
                "cost": "None"
            })

        # Check for database indexes
        if not self._has_indexes():
            medium_impact.append({
                "title": "Add database indexes",
                "current": "Full table scans on queries",
                "expected": "100x faster query performance",
                "implementation": "2 hours",
                "cost": "None"
            })

        # Check for async processing
        if not self._has_async_processing():
            medium_impact.append({
                "title": "Implement async background jobs",
                "current": "Synchronous processing blocks requests",
                "expected": "Faster response times, better UX",
                "implementation": "5 hours",
                "cost": "None"
            })

        # Check for CDN
        if not self._has_cdn():
            low_impact.append({
                "title": "Add CDN for static assets",
                "current": "Static assets served from application server",
                "expected": "30-50% faster asset loading",
                "implementation": "2 hours",
                "cost": "+$10/month"
            })

        # Check for compression
        if not self._has_compression():
            low_impact.append({
                "title": "Enable gzip compression",
                "current": "Uncompressed responses",
                "expected": "60-80% smaller payload sizes",
                "implementation": "1 hour",
                "cost": "None"
            })

        return high_impact, medium_impact, low_impact

    def _has_caching(self):
        """Check for caching implementation"""
        return self._contains_technology(PERFORMANCE_INDICATORS['caching'])

    def _has_connection_pooling(self):
        """Check for database connection pooling"""
        return self._contains_technology(PERFORMANCE_INDICATORS['connection_pooling'])

    def _has_async_processing(self):
        """Check for async/background job processing"""
        return self._contains_technology(PERFORMANCE_INDICATORS['async_processing'])

    def _has_indexes(self):
        """Check for database indexes"""
        return self._contains_technology(
            PERFORMANCE_INDICATORS['database_indexes'],
            ['.sql', '.py', '.rb', '.js']
        )

    def _has_n_plus_one_queries(self):
        """Check for potential N+1 query problems"""
        code_files = self._get_code_files()

        for file_path in code_files:
            content = self._read_file_safe(file_path)
            if content:
                # Check each N+1 pattern
                for pattern in N_PLUS_ONE_PATTERNS:
                    if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
                        return True

        return False

    def _has_cdn(self):
        """Check for CDN usage"""
        return self._contains_technology(PERFORMANCE_INDICATORS['cdn'])

    def _has_compression(self):
        """Check for response compression"""
        return self._contains_technology(
            PERFORMANCE_INDICATORS['compression'],
            ['.conf', '.yml', '.yaml', '.js', '.py']
        )


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 performance_analyzer.py <project_path>")
        sys.exit(1)

    analyzer = PerformanceAnalyzer(sys.argv[1])
    results = analyzer.analyze()
    print(json.dumps(results, indent=2))
