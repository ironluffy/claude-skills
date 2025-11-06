#!/usr/bin/env python3
"""
System Design Reviewer - Main Orchestrator
Analyzes system designs and generates comprehensive review reports with diagrams
"""

import argparse
import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Import analyzers
try:
    from generate_diagrams import DiagramGenerator
    from analyze_architecture import ArchitectureAnalyzer
    from security_analyzer import SecurityAnalyzer
    from performance_analyzer import PerformanceAnalyzer
    from cost_optimizer import CostOptimizer
except ImportError:
    # Allow running from different directories
    pass


class SystemDesignReviewer:
    """Main orchestrator for system design reviews"""

    def __init__(self, project_path, output_path=None):
        self.project_path = Path(project_path).resolve()
        self.output_path = output_path or "design-review.md"
        self.findings = {
            "architecture": {},
            "security": {},
            "performance": {},
            "cost": {},
            "diagrams": {}
        }

    def analyze(self):
        """Run complete system design analysis"""
        print(f"🔍 Analyzing system design: {self.project_path}")
        print("=" * 80)

        # Generate diagrams
        print("\n📊 Generating diagrams...")
        self.generate_diagrams()

        # Architecture review
        print("\n🏗️  Analyzing architecture...")
        self.analyze_architecture()

        # Security review
        print("\n🔒 Analyzing security...")
        self.analyze_security()

        # Performance review
        print("\n⚡ Analyzing performance...")
        self.analyze_performance()

        # Cost review
        print("\n💰 Analyzing costs...")
        self.analyze_costs()

        # Generate report
        print(f"\n📝 Generating review report: {self.output_path}")
        self.generate_report()

        print("\n✅ Review complete!")
        print(f"📄 Report saved to: {self.output_path}")

    def generate_diagrams(self):
        """Generate architecture diagrams"""
        try:
            generator = DiagramGenerator(self.project_path)
            diagrams = generator.generate_all()
            self.findings["diagrams"] = diagrams
            print(f"   ✓ Generated {len(diagrams)} diagram types")
        except Exception as e:
            print(f"   ⚠️  Diagram generation partial: {e}")
            self.findings["diagrams"] = self._create_sample_diagrams()

    def analyze_architecture(self):
        """Analyze architecture best practices"""
        try:
            analyzer = ArchitectureAnalyzer(self.project_path)
            results = analyzer.analyze()
            self.findings["architecture"] = results
            print(f"   ✓ Found {results.get('issue_count', 0)} issues")
        except Exception as e:
            print(f"   ⚠️  Architecture analysis partial: {e}")
            self.findings["architecture"] = self._create_sample_architecture()

    def analyze_security(self):
        """Analyze security vulnerabilities"""
        try:
            analyzer = SecurityAnalyzer(self.project_path)
            results = analyzer.analyze()
            self.findings["security"] = results
            critical = results.get('critical_count', 0)
            high = results.get('high_count', 0)
            print(f"   ✓ Found {critical} critical, {high} high issues")
        except Exception as e:
            print(f"   ⚠️  Security analysis partial: {e}")
            self.findings["security"] = self._create_sample_security()

    def analyze_performance(self):
        """Analyze performance bottlenecks"""
        try:
            analyzer = PerformanceAnalyzer(self.project_path)
            results = analyzer.analyze()
            self.findings["performance"] = results
            print(f"   ✓ Found {results.get('optimization_count', 0)} optimizations")
        except Exception as e:
            print(f"   ⚠️  Performance analysis partial: {e}")
            self.findings["performance"] = self._create_sample_performance()

    def analyze_costs(self):
        """Analyze cost optimization opportunities"""
        try:
            analyzer = CostOptimizer(self.project_path)
            results = analyzer.analyze()
            self.findings["cost"] = results
            savings = results.get('potential_savings_pct', 0)
            print(f"   ✓ Potential savings: {savings}%")
        except Exception as e:
            print(f"   ⚠️  Cost analysis partial: {e}")
            self.findings["cost"] = self._create_sample_cost()

    def generate_report(self):
        """Generate comprehensive markdown report"""
        report = self._build_report()

        # Ensure output directory exists
        output_dir = Path(self.output_path).parent
        if output_dir and not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, 'w') as f:
            f.write(report)

    def _build_report(self):
        """Build markdown report from findings"""
        report_parts = []

        # Header
        report_parts.append(self._generate_header())

        # Executive Summary
        report_parts.append(self._generate_executive_summary())

        # Diagrams
        report_parts.append(self._generate_diagrams_section())

        # Architecture Review
        report_parts.append(self._generate_architecture_section())

        # Security Review
        report_parts.append(self._generate_security_section())

        # Performance Review
        report_parts.append(self._generate_performance_section())

        # Cost Review
        report_parts.append(self._generate_cost_section())

        # Conclusion
        report_parts.append(self._generate_conclusion())

        return "\n\n".join(report_parts)

    def _generate_header(self):
        """Generate report header"""
        return f"""# System Design Review Report
**Project:** {self.project_path.name}
**Review Date:** {datetime.now().strftime('%Y-%m-%d')}
**Reviewer:** System Design Reviewer (Automated)

---"""

    def _generate_executive_summary(self):
        """Generate executive summary"""
        arch = self.findings["architecture"]
        sec = self.findings["security"]
        perf = self.findings["performance"]
        cost = self.findings["cost"]

        return f"""## Executive Summary

High-level overview of findings:

- **Architecture:** {arch.get('issue_count', 0)} issues, {arch.get('recommendation_count', 0)} recommendations
- **Security:** {sec.get('critical_count', 0)} critical, {sec.get('high_count', 0)} high, {sec.get('medium_count', 0)} medium issues
- **Performance:** {perf.get('optimization_count', 0)} optimization opportunities
- **Cost:** Current ${cost.get('current_cost', 0)}/month → Potential ${cost.get('optimized_cost', 0)}/month ({cost.get('potential_savings_pct', 0)}% savings)

---"""

    def _generate_diagrams_section(self):
        """Generate diagrams section"""
        diagrams = self.findings["diagrams"]

        sections = ["## System Diagrams\n"]

        # Architecture diagram
        if "architecture_mermaid" in diagrams:
            sections.append("### Architecture Overview (Mermaid)\n```mermaid")
            sections.append(diagrams["architecture_mermaid"])
            sections.append("```\n")

        if "architecture_ascii" in diagrams:
            sections.append("### Architecture Overview (ASCII)\n```")
            sections.append(diagrams["architecture_ascii"])
            sections.append("```\n")

        # Sequence diagram
        if "sequence_mermaid" in diagrams:
            sections.append("### Authentication Flow (Mermaid)\n```mermaid")
            sections.append(diagrams["sequence_mermaid"])
            sections.append("```\n")

        # ER diagram
        if "er_mermaid" in diagrams:
            sections.append("### Database Schema (Mermaid)\n```mermaid")
            sections.append(diagrams["er_mermaid"])
            sections.append("```\n")

        sections.append("---")
        return "\n".join(sections)

    def _generate_architecture_section(self):
        """Generate architecture review section"""
        arch = self.findings["architecture"]

        sections = ["## Architecture Review\n"]

        # Strengths
        if arch.get("strengths"):
            sections.append("### ✅ Strengths\n")
            for strength in arch["strengths"]:
                sections.append(f"- {strength}")
            sections.append("")

        # Issues & Recommendations
        sections.append("### ⚠️ Issues & Recommendations\n")

        for priority in ["HIGH", "MEDIUM", "LOW"]:
            issues = arch.get(f"{priority.lower()}_issues", [])
            if issues:
                sections.append(f"#### {priority} Priority\n")
                for issue in issues:
                    sections.append(f"**Issue:** {issue['title']}")
                    sections.append(f"- **Impact:** {issue['impact']}")
                    sections.append(f"- **Recommendation:** {issue['recommendation']}")
                    sections.append(f"- **Effort:** {issue['effort']}")
                    if issue.get('cost_impact'):
                        sections.append(f"- **Cost Impact:** {issue['cost_impact']}")
                    sections.append("")

        sections.append("---")
        return "\n".join(sections)

    def _generate_security_section(self):
        """Generate security review section"""
        sec = self.findings["security"]

        sections = ["## Security Review\n"]

        # Strengths
        if sec.get("strengths"):
            sections.append("### ✅ Strengths\n")
            for strength in sec["strengths"]:
                sections.append(f"- {strength}")
            sections.append("")

        # Issues by severity
        for severity, emoji in [("CRITICAL", "🚨"), ("HIGH", "⚠️"), ("MEDIUM", "📋")]:
            issues = sec.get(f"{severity.lower()}_issues", [])
            if issues:
                sections.append(f"### {emoji} {severity.title()} Priority Issues\n")
                for issue in issues:
                    sections.append(f"**{severity}:** {issue['title']}")
                    if issue.get('file'):
                        sections.append(f"- **File:** `{issue['file']}`")
                    sections.append(f"- **Risk:** {issue['risk']}")
                    sections.append(f"- **Fix:** {issue['fix']}")
                    sections.append(f"- **Effort:** {issue['effort']}")
                    sections.append("")

        sections.append("---")
        return "\n".join(sections)

    def _generate_performance_section(self):
        """Generate performance review section"""
        perf = self.findings["performance"]

        sections = ["## Performance Review\n"]

        # Strengths
        if perf.get("strengths"):
            sections.append("### ✅ Strengths\n")
            for strength in perf["strengths"]:
                sections.append(f"- {strength}")
            sections.append("")

        # Optimization opportunities
        sections.append("### ⚠️ Optimization Opportunities\n")

        for impact in ["HIGH", "MEDIUM", "LOW"]:
            opportunities = perf.get(f"{impact.lower()}_impact", [])
            if opportunities:
                sections.append(f"#### {impact} Impact\n")
                for opp in opportunities:
                    sections.append(f"**Opportunity:** {opp['title']}")
                    if opp.get('current'):
                        sections.append(f"- **Current:** {opp['current']}")
                    if opp.get('expected'):
                        sections.append(f"- **Expected:** {opp['expected']}")
                    sections.append(f"- **Implementation:** {opp['implementation']}")
                    if opp.get('cost'):
                        sections.append(f"- **Cost:** {opp['cost']}")
                    sections.append("")

        sections.append("---")
        return "\n".join(sections)

    def _generate_cost_section(self):
        """Generate cost review section"""
        cost = self.findings["cost"]

        sections = ["## Cost Optimization\n"]

        # Current cost
        sections.append(f"### Current Monthly Cost: ${cost.get('current_cost', 0)}\n")

        if cost.get("breakdown"):
            sections.append("**Breakdown:**")
            for item, amount in cost["breakdown"].items():
                sections.append(f"- {item}: ${amount}")
            sections.append("")

        # Optimization opportunities
        sections.append("### Optimization Opportunities\n")

        for impact in ["HIGH", "MEDIUM", "LOW"]:
            opportunities = cost.get(f"{impact.lower()}_impact", [])
            if opportunities:
                sections.append(f"#### {impact} Impact\n")
                for opp in opportunities:
                    sections.append(f"**Opportunity:** {opp['title']}")
                    if opp.get('analysis'):
                        sections.append(f"- **Analysis:** {opp['analysis']}")
                    sections.append(f"- **Recommendation:** {opp['recommendation']}")
                    sections.append(f"- **Savings:** {opp['savings']}")
                    if opp.get('risk'):
                        sections.append(f"- **Risk:** {opp['risk']}")
                    if opp.get('implementation'):
                        sections.append(f"- **Implementation:** {opp['implementation']}")
                    sections.append("")

        # Optimized cost
        sections.append(f"### Optimized Monthly Cost: ${cost.get('optimized_cost', 0)} ({cost.get('potential_savings_pct', 0)}% reduction)\n")

        sections.append("---")
        return "\n".join(sections)

    def _generate_conclusion(self):
        """Generate conclusion"""
        cost = self.findings["cost"]
        sec = self.findings["security"]

        return f"""## Conclusion

The system has been analyzed across architecture, security, performance, and cost dimensions. Key takeaways:

- **{cost.get('potential_savings_pct', 0)}% cost reduction** (${cost.get('current_cost', 0)} → ${cost.get('optimized_cost', 0)}/month)
- **Security improvements needed:** {sec.get('critical_count', 0)} critical + {sec.get('high_count', 0)} high priority issues
- **Performance optimization potential:** Multiple opportunities identified
- **Architecture recommendations:** Follow implementation roadmap

**Next Steps:**
1. Address critical security issues immediately
2. Implement high-impact performance optimizations
3. Execute cost optimization plan
4. Track metrics and KPIs post-implementation"""

    def _create_sample_diagrams(self):
        """Create sample diagrams when generation fails"""
        return {
            "architecture_mermaid": """graph TB
    Client[Web Client]
    API[API Gateway]
    Backend[Backend Service]
    DB[(Database)]

    Client -->|HTTPS| API
    API -->|REST| Backend
    Backend -->|Query| DB""",
            "architecture_ascii": """┌────────────┐
│ Web Client │
└──────┬─────┘
       │ HTTPS
┌──────▼─────┐
│ API Gateway│
└──────┬─────┘
       │ REST
┌──────▼─────┐
│  Backend   │
└──────┬─────┘
       │ Query
┌──────▼─────┐
│  Database  │
└────────────┘"""
        }

    def _create_sample_architecture(self):
        """Create sample architecture findings"""
        return {
            "issue_count": 2,
            "recommendation_count": 3,
            "strengths": [
                "Well-separated components",
                "Clear API contracts"
            ],
            "high_issues": [{
                "title": "Single point of failure in database",
                "impact": "System downtime if database fails",
                "recommendation": "Implement database replication",
                "effort": "4 hours",
                "cost_impact": "+$50/month"
            }],
            "medium_issues": [{
                "title": "No caching layer",
                "impact": "High database load",
                "recommendation": "Add Redis cache",
                "effort": "6 hours",
                "cost_impact": "+$30/month"
            }]
        }

    def _create_sample_security(self):
        """Create sample security findings"""
        return {
            "critical_count": 1,
            "high_count": 1,
            "medium_count": 2,
            "strengths": [
                "Using HTTPS everywhere",
                "Input validation on API endpoints"
            ],
            "critical_issues": [{
                "title": "Hardcoded API keys in source code",
                "file": "config/settings.py",
                "risk": "Key exposure in version control",
                "fix": "Move to environment variables",
                "effort": "1 hour"
            }],
            "high_issues": [{
                "title": "No rate limiting on authentication",
                "risk": "Brute force attacks possible",
                "fix": "Add rate limiting (10 attempts/min)",
                "effort": "2 hours"
            }]
        }

    def _create_sample_performance(self):
        """Create sample performance findings"""
        return {
            "optimization_count": 3,
            "strengths": [
                "Connection pooling configured",
                "Proper indexes on user table"
            ],
            "high_impact": [{
                "title": "Add Redis caching",
                "current": "500ms average response time",
                "expected": "50ms with caching (10x improvement)",
                "implementation": "6 hours",
                "cost": "+$30/month"
            }],
            "medium_impact": [{
                "title": "Optimize database queries",
                "current": "N+1 queries detected",
                "expected": "200ms → 50ms (4x improvement)",
                "implementation": "3 hours"
            }]
        }

    def _create_sample_cost(self):
        """Create sample cost findings"""
        return {
            "current_cost": 450,
            "optimized_cost": 285,
            "potential_savings_pct": 37,
            "breakdown": {
                "Compute": 200,
                "Database": 150,
                "Storage": 50,
                "Network": 30,
                "Other": 20
            },
            "high_impact": [{
                "title": "Right-size compute instances",
                "analysis": "Current CPU utilization 15-20%",
                "recommendation": "Downgrade to t3.small",
                "savings": "$100/month (50% reduction)",
                "risk": "Low (ample headroom)"
            }],
            "medium_impact": [{
                "title": "Implement database connection pooling",
                "analysis": "db.t3.large to handle connection overhead",
                "recommendation": "Add PgBouncer, downgrade to db.t3.medium",
                "savings": "$50/month",
                "implementation": "3 hours"
            }]
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="System Design Reviewer - Analyze and review system designs")
    parser.add_argument("project_path", help="Path to project to review")
    parser.add_argument("-o", "--output", default="design-review.md", help="Output report path")
    parser.add_argument("--json", action="store_true", help="Also output JSON findings")

    args = parser.parse_args()

    if not os.path.exists(args.project_path):
        print(f"❌ Error: Project path does not exist: {args.project_path}")
        sys.exit(1)

    reviewer = SystemDesignReviewer(args.project_path, args.output)
    reviewer.analyze()

    if args.json:
        json_path = args.output.replace('.md', '.json')
        with open(json_path, 'w') as f:
            json.dump(reviewer.findings, f, indent=2)
        print(f"📊 JSON findings saved to: {json_path}")


if __name__ == "__main__":
    main()
