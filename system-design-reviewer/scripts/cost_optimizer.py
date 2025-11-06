#!/usr/bin/env python3
"""
Cost Optimizer - Analyze cloud costs and identify optimization opportunities
"""

import os
import re
from pathlib import Path


class CostOptimizer:
    """Analyze cloud cost optimization opportunities"""

    def __init__(self, project_path):
        self.project_path = Path(project_path)

    def analyze(self):
        """Run cost optimization analysis"""
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
            "breakdown": self._get_cost_breakdown(current_cost),
            "high_impact": optimizations.get('high', []),
            "medium_impact": optimizations.get('medium', []),
            "low_impact": optimizations.get('low', [])
        }

        return results

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
        return any(self.project_path.rglob("kubernetes.yml")) or \
               any(self.project_path.rglob("k8s/*")) or \
               any(self.project_path.rglob("*.k8s.yaml"))

    def _has_load_balancer(self):
        """Check for load balancer"""
        lb_indicators = ['loadbalancer', 'alb', 'elb', 'nginx', 'haproxy']
        for file in self.project_path.rglob("*"):
            if any(indicator in file.name.lower() for indicator in lb_indicators):
                return True
        return False

    def _has_cdn(self):
        """Check for CDN"""
        cdn_indicators = ['cloudfront', 'cloudflare', 'cdn']
        for file in self.project_path.rglob("*"):
            try:
                content = file.read_text().lower()
                if any(indicator in content for indicator in cdn_indicators):
                    return True
            except Exception:
                continue
        return False

    def _has_multiple_databases(self):
        """Check for multiple databases"""
        db_files = list(self.project_path.rglob("*database*")) + \
                   list(self.project_path.rglob("*db*"))
        return len(db_files) > 3

    def _is_over_provisioned(self):
        """Check if infrastructure appears over-provisioned"""
        # Look for large instance types
        large_instances = ['xlarge', '2xlarge', '4xlarge', 'large']
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.yml', '.yaml', '.tf', '.json']:
                try:
                    content = file.read_text().lower()
                    if any(instance in content for instance in large_instances):
                        return True
                except Exception:
                    continue
        return False

    def _has_serverless_opportunity(self):
        """Check if serverless would be beneficial"""
        # Look for API-only applications
        has_api = any(self.project_path.rglob("*api*"))
        has_simple_structure = len(list(self.project_path.rglob("*.py"))) < 20
        return has_api and has_simple_structure

    def _has_database_optimization(self):
        """Check for database optimization opportunities"""
        # Assume there's always room for database optimization
        return True

    def _has_storage_lifecycle(self):
        """Check for storage lifecycle policies"""
        lifecycle_indicators = ['lifecycle', 'archiv', 'glacier', 'cold.storage']
        for file in self.project_path.rglob("*"):
            try:
                content = file.read_text().lower()
                if any(indicator.replace('.', r'[\s_-]?') in content for indicator in lifecycle_indicators):
                    return True
            except Exception:
                continue
        return False

    def _uses_reserved_instances(self):
        """Check if reserved instances are used"""
        reserved_indicators = ['reserved', 'savings.plan']
        for file in self.project_path.rglob("*"):
            try:
                content = file.read_text().lower()
                if any(indicator.replace('.', r'[\s_-]?') in content for indicator in reserved_indicators):
                    return True
            except Exception:
                continue
        return False

    def _has_unused_resources(self):
        """Check for potentially unused resources"""
        # Heuristic: If there are old config files, there might be unused resources
        old_configs = ['old', 'backup', 'deprecated', 'unused', 'temp']
        for file in self.project_path.rglob("*"):
            if any(keyword in file.name.lower() for keyword in old_configs):
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
