"""
Report Generator - HTML report generation for system design reviews
Part of system-design-reviewer skill for Claude Skills

Generates professional HTML reports with architecture, security, performance,
and cost optimization findings.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from report_base import HTMLReportBase, ReportSection

from constants import SEVERITY_COLORS, STRENGTH_ICONS


class SystemDesignReportGenerator(HTMLReportBase):
    """Generate professional HTML reports for system design reviews

    Extends HTMLReportBase with system design-specific styling and sections.
    """

    # Extended CSS for system design reports
    EXTENDED_STYLE = """
    <style>
        .issue-card {
            border-left: 4px solid #ccc;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
            background: #fafafa;
        }
        .issue-card.critical {
            border-left-color: #dc3545;
            background: #fff5f5;
        }
        .issue-card.high {
            border-left-color: #fd7e14;
            background: #fff9f5;
        }
        .issue-card.medium {
            border-left-color: #ffc107;
            background: #fffef5;
        }
        .issue-card.low {
            border-left-color: #17a2b8;
            background: #f5fcff;
        }
        .issue-card.success {
            border-left-color: #28a745;
            background: #f5fff5;
        }
        .issue-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .badge.critical { background: #dc3545; color: white; }
        .badge.high { background: #fd7e14; color: white; }
        .badge.medium { background: #ffc107; color: #333; }
        .badge.low { background: #17a2b8; color: white; }
        .badge.success { background: #28a745; color: white; }
        .summary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin: 30px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .summary h2 { color: white; border: none; margin: 0 0 20px 0; padding: 0; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-card {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .stat-label {
            font-size: 1em;
            opacity: 0.9;
        }
        .strengths-section {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin: 30px 0;
        }
        .strengths-section h3 {
            color: white;
            margin-top: 0;
        }
        .strengths-list {
            list-style: none;
            padding: 0;
        }
        .strengths-list li {
            padding: 10px 0;
            font-size: 1.1em;
        }
        .strengths-list li:before {
            content: "✓";
            margin-right: 10px;
            font-weight: bold;
        }
        details {
            margin: 15px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 4px;
        }
        summary {
            cursor: pointer;
            font-weight: bold;
            padding: 10px;
            background: #eee;
            border-radius: 4px;
            margin: -15px -15px 15px -15px;
        }
        summary:hover { background: #ddd; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th {
            background: #0066cc;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover { background: #f9f9f9; }
    </style>
    """

    def __init__(self, title: str = "System Design Review Report", description: str = ""):
        super().__init__(title, description)
        self.BASE_STYLE += self.EXTENDED_STYLE

    def add_summary_stats(self, stats: Dict[str, int]) -> None:
        """Add summary statistics section

        Args:
            stats: Dictionary of statistic labels to values
        """
        html = '<div class="stats">'

        for label, value in stats.items():
            # Determine color based on label
            if 'critical' in label.lower() or 'high' in label.lower():
                color = 'rgba(220, 53, 69, 0.3)'
            elif 'medium' in label.lower():
                color = 'rgba(255, 193, 7, 0.3)'
            elif 'low' in label.lower():
                color = 'rgba(23, 162, 184, 0.3)'
            else:
                color = 'rgba(255, 255, 255, 0.2)'

            html += f'''
            <div class="stat-card" style="background: {color};">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            '''

        html += '</div>'

        self.add_section(ReportSection(
            title="Summary Statistics",
            content=html
        ))

    def add_strengths(self, strengths: List[str], category: str = "System") -> None:
        """Add strengths section

        Args:
            strengths: List of strength descriptions
            category: Category name (e.g., "Architecture", "Security")
        """
        if not strengths:
            return

        icon = STRENGTH_ICONS.get(category.lower(), '✓')

        html = f'''
        <div class="strengths-section">
            <h3>{icon} {category} Strengths</h3>
            <ul class="strengths-list">
        '''

        for strength in strengths:
            html += f'<li>{strength}</li>\n'

        html += '''
            </ul>
        </div>
        '''

        self.add_section(ReportSection(
            title=f"{category} Strengths",
            content=html,
            severity='success'
        ))

    def add_issues(self, issues: List[Dict], severity: str, category: str = "") -> None:
        """Add issues section

        Args:
            issues: List of issue dictionaries
            severity: Severity level ('critical', 'high', 'medium', 'low')
            category: Optional category name
        """
        if not issues:
            return

        for issue in issues:
            content = self._format_issue_content(issue)
            title = issue.get('title', 'Issue')
            if category:
                title = f"{category}: {title}"

            self.add_section(ReportSection(
                title=title,
                content=content,
                severity=severity
            ))

    def _format_issue_content(self, issue: Dict) -> str:
        """Format issue content for display

        Args:
            issue: Issue dictionary

        Returns:
            str: Formatted HTML content
        """
        html = '<div class="metadata">'

        # Add impact/risk
        if 'impact' in issue:
            html += f'<div class="metadata-item"><span class="metadata-label">Impact:</span> {issue["impact"]}</div>'
        if 'risk' in issue:
            html += f'<div class="metadata-item"><span class="metadata-label">Risk:</span> {issue["risk"]}</div>'

        # Add file reference if present
        if 'file' in issue:
            html += f'<div class="metadata-item"><span class="metadata-label">File:</span> <code>{issue["file"]}</code></div>'

        # Add effort and cost
        if 'effort' in issue:
            html += f'<div class="metadata-item"><span class="metadata-label">Effort:</span> {issue["effort"]}</div>'
        if 'cost_impact' in issue:
            html += f'<div class="metadata-item"><span class="metadata-label">Cost Impact:</span> {issue["cost_impact"]}</div>'

        html += '</div>'

        # Add recommendation/fix
        if 'recommendation' in issue:
            html += f'<h3>Recommendation</h3><p>{issue["recommendation"]}</p>'
        if 'fix' in issue:
            html += f'<h3>How to Fix</h3><p>{issue["fix"]}</p>'

        # Add implementation details if present
        if 'implementation' in issue:
            html += f'<details><summary><strong>Implementation Details</strong></summary><p>{issue["implementation"]}</p></details>'

        # Add current vs expected for performance issues
        if 'current' in issue and 'expected' in issue:
            html += f'''
            <h3>Performance Impact</h3>
            <table>
                <tr>
                    <th>Current State</th>
                    <th>Expected After Fix</th>
                </tr>
                <tr>
                    <td>{issue["current"]}</td>
                    <td>{issue["expected"]}</td>
                </tr>
            </table>
            '''

        return html

    def _render_section(self, section: ReportSection) -> str:
        """Render a single section with custom styling

        Args:
            section: ReportSection to render

        Returns:
            str: Rendered HTML
        """
        severity_class = f' {section.severity}' if section.severity else ''

        html = f'<div class="issue-card{severity_class}">\n'

        if section.severity and section.severity != 'success':
            badge = f'<span class="badge {section.severity}">{section.severity}</span>'
            html += f'    <div class="issue-title">{badge} {section.title}</div>\n'
        else:
            html += f'    <h2>{section.title}</h2>\n'

        html += f'    {section.content}\n'
        html += '</div>\n'

        return html


def generate_full_review_report(
    output_path: Path,
    architecture_results: Optional[Dict] = None,
    security_results: Optional[Dict] = None,
    performance_results: Optional[Dict] = None,
    cost_results: Optional[Dict] = None,
    metadata: Optional[Dict] = None
) -> None:
    """Generate a complete system design review report

    Args:
        output_path: Path to save HTML report
        architecture_results: Architecture analysis results
        security_results: Security analysis results
        performance_results: Performance analysis results
        cost_results: Cost optimization results
        metadata: Additional metadata to include
    """
    report = SystemDesignReportGenerator(
        title="Complete System Design Review",
        description="Comprehensive analysis of architecture, security, performance, and cost optimization"
    )

    # Add metadata
    if metadata:
        for key, value in metadata.items():
            report.add_metadata(key, value)

    # Calculate and add summary statistics
    stats = {}
    total_issues = 0

    if architecture_results:
        stats['Architecture Issues'] = architecture_results.get('issue_count', 0)
        total_issues += architecture_results.get('issue_count', 0)

    if security_results:
        critical = security_results.get('critical_count', 0)
        high = security_results.get('high_count', 0)
        stats['Security Critical'] = critical
        stats['Security High'] = high
        total_issues += critical + high + security_results.get('medium_count', 0)

    if performance_results:
        stats['Performance Optimizations'] = performance_results.get('optimization_count', 0)
        total_issues += performance_results.get('optimization_count', 0)

    if cost_results:
        stats['Cost Savings'] = cost_results.get('savings_count', 0)

    stats['Total Recommendations'] = total_issues

    if stats:
        report.add_summary_stats(stats)

    # Add architecture results
    if architecture_results:
        if architecture_results.get('strengths'):
            report.add_strengths(architecture_results['strengths'], 'Architecture')

        report.add_issues(architecture_results.get('high_issues', []), 'high', 'Architecture')
        report.add_issues(architecture_results.get('medium_issues', []), 'medium', 'Architecture')
        report.add_issues(architecture_results.get('low_issues', []), 'low', 'Architecture')

    # Add security results
    if security_results:
        if security_results.get('strengths'):
            report.add_strengths(security_results['strengths'], 'Security')

        report.add_issues(security_results.get('critical_issues', []), 'critical', 'Security')
        report.add_issues(security_results.get('high_issues', []), 'high', 'Security')
        report.add_issues(security_results.get('medium_issues', []), 'medium', 'Security')

    # Add performance results
    if performance_results:
        if performance_results.get('strengths'):
            report.add_strengths(performance_results['strengths'], 'Performance')

        report.add_issues(performance_results.get('high_impact', []), 'high', 'Performance')
        report.add_issues(performance_results.get('medium_impact', []), 'medium', 'Performance')
        report.add_issues(performance_results.get('low_impact', []), 'low', 'Performance')

    # Add cost results
    if cost_results:
        if cost_results.get('strengths'):
            report.add_strengths(cost_results['strengths'], 'Cost')

        report.add_issues(cost_results.get('high_savings', []), 'high', 'Cost Optimization')
        report.add_issues(cost_results.get('medium_savings', []), 'medium', 'Cost Optimization')

    # Save report
    report.save(output_path)


# Example usage
if __name__ == '__main__':
    # Example: Create a sample system design review report
    report = SystemDesignReportGenerator(
        title="Example System Design Review",
        description="Sample report showing system design review capabilities"
    )

    report.add_metadata('Project', 'Example Application')
    report.add_metadata('Reviewed By', 'System Design Reviewer')

    # Add summary statistics
    report.add_summary_stats({
        'Architecture Issues': 5,
        'Security Critical': 2,
        'Performance Optimizations': 8,
        'Total Recommendations': 15
    })

    # Add strengths
    report.add_strengths([
        'Well-separated components (MVC pattern)',
        'Test infrastructure in place',
        'Containerized application (Docker)'
    ], 'Architecture')

    # Add a critical security issue
    report.add_issues([{
        'title': 'Hardcoded API keys in source code',
        'risk': 'API key exposure in version control',
        'fix': 'Move to environment variables or secret management',
        'effort': '1 hour',
        'file': 'src/config.py'
    }], 'critical', 'Security')

    # Save report
    report.save(Path('example_system_design_report.html'))
    print("Example report generated: example_system_design_report.html")
