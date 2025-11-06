#!/usr/bin/env python3
"""
Performance Analyzer - Identify performance bottlenecks and optimization opportunities
"""

import os
import re
from pathlib import Path


class PerformanceAnalyzer:
    """Analyze performance bottlenecks"""

    def __init__(self, project_path):
        self.project_path = Path(project_path)

    def analyze(self):
        """Run performance analysis"""
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
        cache_indicators = ['redis', 'memcache', 'cache']
        for file in self.project_path.rglob("*"):
            if file.is_file():
                try:
                    if any(indicator in file.name.lower() for indicator in cache_indicators):
                        return True
                    if file.suffix in ['.py', '.js', '.java', '.go']:
                        content = file.read_text().lower()
                        if any(f"{indicator}" in content for indicator in cache_indicators):
                            return True
                except Exception:
                    continue
        return False

    def _has_connection_pooling(self):
        """Check for database connection pooling"""
        pool_patterns = ['connection.pool', 'pool.size', 'max.connections', 'pooling']
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.py', '.js', '.java', '.conf', '.yml', '.yaml']:
                try:
                    content = file.read_text().lower()
                    if any(pattern.replace('.', r'[\s_-]?') in content for pattern in pool_patterns):
                        return True
                except Exception:
                    continue
        return False

    def _has_async_processing(self):
        """Check for async/background job processing"""
        async_indicators = ['celery', 'rq', 'sidekiq', 'bull', 'async', 'await', 'queue', 'worker']
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.py', '.js', '.java', '.go']:
                try:
                    content = file.read_text().lower()
                    if any(indicator in content for indicator in async_indicators):
                        return True
                except Exception:
                    continue
        return False

    def _has_indexes(self):
        """Check for database indexes"""
        index_patterns = ['create.index', 'index.on', '@index', 'add_index']
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.sql', '.py', '.rb', '.js']:
                try:
                    content = file.read_text().lower()
                    if any(pattern.replace('.', r'[\s_]') in content for pattern in index_patterns):
                        return True
                except Exception:
                    continue
        return False

    def _has_n_plus_one_queries(self):
        """Check for potential N+1 query problems"""
        # This is a heuristic check - looks for loops with database queries
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.py', '.js', '.rb', '.java']:
                try:
                    content = file.read_text()
                    # Look for loops with query keywords
                    if re.search(r'for\s+.*\sin\s+.*:.*(?:query|find|get|select)', content, re.DOTALL | re.IGNORECASE):
                        return True
                except Exception:
                    continue
        return False

    def _has_cdn(self):
        """Check for CDN usage"""
        cdn_patterns = ['cloudfront', 'cloudflare', 'akamai', 'fastly', 'cdn']
        for file in self.project_path.rglob("*"):
            try:
                content = file.read_text().lower()
                if any(pattern in content for pattern in cdn_patterns):
                    return True
            except Exception:
                continue
        return False

    def _has_compression(self):
        """Check for response compression"""
        compression_patterns = ['gzip', 'compress', 'deflate', 'brotli']
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.conf', '.yml', '.yaml', '.js', '.py']:
                try:
                    content = file.read_text().lower()
                    if any(pattern in content for pattern in compression_patterns):
                        return True
                except Exception:
                    continue
        return False


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 performance_analyzer.py <project_path>")
        sys.exit(1)

    analyzer = PerformanceAnalyzer(sys.argv[1])
    results = analyzer.analyze()
    print(json.dumps(results, indent=2))
