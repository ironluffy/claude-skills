#!/usr/bin/env python3
"""
Cost Optimizer - Analyze cloud costs and identify optimization opportunities
Part of system-design-reviewer skill for Claude Skills

Refactored to use BaseAnalyzer and shared utilities.
"""

from pathlib import Path

from analyzer_base import BaseAnalyzer
from constants import CLOUD_SERVICE_PATTERNS, INSTANCE_SIZES


class CostOptimizer(BaseAnalyzer):
    """Analyze cloud cost optimization opportunities"""

    def analyze(self):
        """Run cost optimization analysis"""
        self._log_analysis_start("Cost Optimization")

        # Estimate current costs based on infrastructure
        current_cost = self._estimate_current_cost()
        optimizations = self._find_optimizations()

        # Calculate potential savings
        total_savings = sum(opt.get('savings_amount', 0) for opts in optimizations.values() for opt in opts)
        optimized_cost = max(0, current_cost - total_savings)
        savings_pct = int((total_savings / current_cost * 100)) if current_cost > 0 else 0

        results = {
            "current_cost": current_cost,
            "optimized_cost": optimized_cost,
            "potential_savings_pct": savings_pct,
            "savings_count": len(optimizations['high']) + len(optimizations['medium']) + len(optimizations['low']),
            "breakdown": self._get_cost_breakdown(current_cost),
            "strengths": self._find_strengths(),
            "high_savings": optimizations.get('high', []),
            "medium_savings": optimizations.get('medium', []),
            "low_savings": optimizations.get('low', [])
        }

        self._log_analysis_complete(results)

        return results

    def _find_strengths(self):
        """Find cost optimization strengths"""
        strengths = []

        if self._uses_reserved_instances():
            strengths.append("Using reserved instances for cost savings")

        if self._has_storage_lifecycle():
            strengths.append("Storage lifecycle policies implemented")

        if not self._is_over_provisioned():
            strengths.append("Compute resources appear right-sized")

        return strengths or ["Basic cost management in place"]

    def _estimate_current_cost(self):
        """Estimate current monthly costs"""
        # Base cost estimation based on common infrastructure
        costs = {
            "compute": 200,  # 2x medium instances
            "database": 150,  # Single medium database
            "storage": 50,   # 500GB storage
            "network": 30,   # Data transfer
            "other": 20      # Misc services
        }

        # Adjust based on detected infrastructure
        if self._has_kubernetes():
            costs["compute"] += 150  # Additional nodes
        if self._has_load_balancer():
            costs["network"] += 20
        if self._has_cdn():
            costs["network"] += 10
        if self._has_multiple_databases():
            costs["database"] += 100

        return sum(costs.values())

    def _get_cost_breakdown(self, total):
        """Get cost breakdown by category"""
        return {
            "Compute": int(total * 0.44),
            "Database": int(total * 0.33),
            "Storage": int(total * 0.11),
            "Network": int(total * 0.07),
            "Other": int(total * 0.05)
        }

    def _find_optimizations(self):
        """Find cost optimization opportunities"""
        high_impact = []
        medium_impact = []
        low_impact = []

        # Check for over-provisioned compute
        if self._is_over_provisioned():
            high_impact.append({
                "title": "Right-size compute instances",
                "analysis": "CPU utilization appears low based on instance types",
                "recommendation": "Downgrade to smaller instance types",
                "savings": "$100/month (50% reduction)",
                "savings_amount": 100,
                "risk": "Low (monitor metrics closely)"
            })

        # Check for serverless opportunities
        if self._has_serverless_opportunity():
            high_impact.append({
                "title": "Migrate to serverless architecture",
                "analysis": "Low traffic, unpredictable patterns",
                "recommendation": "Use Lambda/Cloud Functions for APIs",
                "savings": "$80/month (40% compute savings)",
                "savings_amount": 80,
                "risk": "Medium (code changes required)"
            })

        # Check for database optimization
        if self._has_database_optimization():
            medium_impact.append({
                "title": "Optimize database instance",
                "analysis": "Connection pooling can reduce instance size needed",
                "recommendation": "Add PgBouncer and downgrade database",
                "savings": "$50/month",
                "savings_amount": 50,
                "implementation": "3 hours"
            })

        # Check for storage optimization
        if not self._has_storage_lifecycle():
            medium_impact.append({
                "title": "Implement storage lifecycle policies",
                "analysis": "Old logs and backups in expensive storage",
                "recommendation": "Move cold data to cheaper storage tiers",
                "savings": "$20/month",
                "savings_amount": 20,
                "implementation": "2 hours"
            })

        # Check for reserved instances
        if not self._uses_reserved_instances():
            low_impact.append({
                "title": "Purchase reserved instances",
                "analysis": "Long-running predictable workloads",
                "recommendation": "Buy 1-year reserved instances",
                "savings": "$40/month (up to 40% discount)",
                "savings_amount": 40,
                "implementation": "1 hour"
            })

        # Check for unused resources
        if self._has_unused_resources():
            low_impact.append({
                "title": "Clean up unused resources",
                "analysis": "Detected potential unused resources",
                "recommendation": "Audit and remove unused databases, storage, etc.",
                "savings": "$30/month",
                "savings_amount": 30,
                "implementation": "2 hours"
            })

        return {"high": high_impact, "medium": medium_impact, "low": low_impact}

    def _has_kubernetes(self):
        """Check for Kubernetes deployment"""
        patterns = ["kubernetes.yml", "k8s/*", "*.k8s.yaml"]
        for pattern in patterns:
            if self._find_files_by_pattern(pattern):
                return True
        return False

    def _has_load_balancer(self):
        """Check for load balancer"""
        lb_indicators = ['loadbalancer', 'alb', 'elb', 'nginx', 'haproxy']
        return self._contains_technology(lb_indicators)

    def _has_cdn(self):
        """Check for CDN"""
        cdn_indicators = ['cloudfront', 'cloudflare', 'cdn']
        return self._contains_technology(cdn_indicators)

    def _has_multiple_databases(self):
        """Check for multiple databases"""
        db_files = self._find_files_by_pattern("*database*") + self._find_files_by_pattern("*db*")
        return len(db_files) > 3

    def _is_over_provisioned(self):
        """Check if infrastructure appears over-provisioned"""
        config_files = self._get_files_by_extensions(['.yml', '.yaml', '.tf', '.json'])

        for file_path in config_files:
            content = self._read_file_safe(file_path)
            if content:
                content_lower = content.lower()
                if any(instance in content_lower for instance in INSTANCE_SIZES[-3:]):  # large, xlarge, 2xlarge
                    return True

        return False

    def _has_serverless_opportunity(self):
        """Check if serverless would be beneficial"""
        # Look for API-only applications
        has_api = bool(self._find_files_by_pattern("*api*"))
        py_files = self._get_files_by_extensions(['.py'])
        has_simple_structure = len(py_files) < 20
        return has_api and has_simple_structure

    def _has_database_optimization(self):
        """Check for database optimization opportunities"""
        # Assume there's always room for database optimization
        return True

    def _has_storage_lifecycle(self):
        """Check for storage lifecycle policies"""
        lifecycle_indicators = ['lifecycle', 'archiv', 'glacier', 'cold.storage', 'cold_storage']
        return self._contains_technology(lifecycle_indicators)

    def _uses_reserved_instances(self):
        """Check if reserved instances are used"""
        reserved_indicators = ['reserved', 'savings.plan', 'savings_plan']
        return self._contains_technology(reserved_indicators)

    def _has_unused_resources(self):
        """Check for potentially unused resources"""
        # Heuristic: If there are old config files, there might be unused resources
        old_configs = ['old', 'backup', 'deprecated', 'unused', 'temp']
        for keyword in old_configs:
            if self._find_files_by_pattern(f"*{keyword}*"):
                return True
        return False


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 cost_optimizer.py <project_path>")
        sys.exit(1)

    optimizer = CostOptimizer(sys.argv[1])
    results = optimizer.analyze()
    print(json.dumps(results, indent=2))
