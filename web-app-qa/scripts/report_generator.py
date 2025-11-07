"""
Report Generator - HTML report generation utilities
Part of web-app-qa skill for Claude Skills

Provides reusable components for generating professional HTML reports.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ReportSection:
    """Represents a section in a report"""
    title: str
    content: str
    severity: Optional[str] = None  # 'critical', 'warning', 'info', 'success'


class HTMLReportGenerator:
    """Generates professional HTML reports for QA testing"""

    BASE_STYLE = """
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                        'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a1a1a;
            border-bottom: 4px solid #0066cc;
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        h2 {{
            color: #333;
            margin-top: 40px;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-left: 4px solid #0066cc;
            padding-left: 15px;
        }}
        h3 {{
            color: #555;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        .summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin: 30px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .summary h2 {{ color: white; border: none; margin: 0 0 20px 0; padding: 0; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .stat-label {{
            font-size: 1em;
            opacity: 0.9;
        }}
        .issue-card {{
            border-left: 4px solid #ccc;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
            background: #fafafa;
        }}
        .issue-card.critical {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        .issue-card.warning {{
            border-left-color: #ffc107;
            background: #fffef5;
        }}
        .issue-card.info {{
            border-left-color: #17a2b8;
            background: #f5fcff;
        }}
        .issue-card.success {{
            border-left-color: #28a745;
            background: #f5fff5;
        }}
        .issue-title {{
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .badge.critical {{ background: #dc3545; color: white; }}
        .badge.warning {{ background: #ffc107; color: #333; }}
        .badge.info {{ background: #17a2b8; color: white; }}
        .badge.success {{ background: #28a745; color: white; }}
        .metadata {{
            color: #666;
            font-size: 0.95em;
            margin: 15px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .metadata-item {{
            margin: 5px 0;
        }}
        .metadata-label {{
            font-weight: bold;
            display: inline-block;
            min-width: 120px;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background: #0066cc;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{ background: #f9f9f9; }}
        .screenshot {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        details {{
            margin: 15px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        summary {{
            cursor: pointer;
            font-weight: bold;
            padding: 10px;
            background: #eee;
            border-radius: 4px;
            margin: -15px -15px 15px -15px;
        }}
        summary:hover {{ background: #ddd; }}
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #eee;
            border-radius: 15px;
            overflow: hidden;
            margin: 15px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 0.3s ease;
        }}
    </style>
    """

    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.sections: List[ReportSection] = []
        self.metadata: Dict[str, str] = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'generator': 'web-app-qa skill'
        }

    def add_metadata(self, key: str, value: str) -> None:
        """Add metadata to the report"""
        self.metadata[key] = value

    def add_section(self, section: ReportSection) -> None:
        """Add a section to the report"""
        self.sections.append(section)

    def generate_summary_stats(self, stats: Dict[str, Any]) -> str:
        """Generate summary statistics cards"""
        html = '<div class="stats">'

        for label, value in stats.items():
            # Determine color based on label
            if 'fail' in label.lower() or 'error' in label.lower() or 'critical' in label.lower():
                color = 'rgba(220, 53, 69, 0.3)'
            elif 'warn' in label.lower():
                color = 'rgba(255, 193, 7, 0.3)'
            elif 'pass' in label.lower() or 'success' in label.lower():
                color = 'rgba(40, 167, 69, 0.3)'
            else:
                color = 'rgba(255, 255, 255, 0.2)'

            html += f'''
            <div class="stat-card" style="background: {color};">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            '''

        html += '</div>'
        return html

    def generate_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        cell_classes: Optional[List[List[str]]] = None
    ) -> str:
        """Generate an HTML table"""
        html = '<table><thead><tr>'

        for header in headers:
            html += f'<th>{header}</th>'

        html += '</tr></thead><tbody>'

        for i, row in enumerate(rows):
            html += '<tr>'
            for j, cell in enumerate(row):
                cell_class = ''
                if cell_classes and i < len(cell_classes) and j < len(cell_classes[i]):
                    cell_class = f' class="{cell_classes[i][j]}"'
                html += f'<td{cell_class}>{cell}</td>'
            html += '</tr>'

        html += '</tbody></table>'
        return html

    def generate_progress_bar(self, percentage: float, label: str = "") -> str:
        """Generate a progress bar"""
        return f'''
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%;">
                {label or f"{percentage:.1f}%"}
            </div>
        </div>
        '''

    def generate(self) -> str:
        """Generate the complete HTML report"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    {self.BASE_STYLE}
</head>
<body>
    <div class="container">
        <h1>{self.title}</h1>
"""

        if self.description:
            html += f'        <p style="font-size: 1.1em; color: #666; margin-bottom: 30px;">{self.description}</p>\n'

        # Add metadata
        html += '        <div class="metadata">\n'
        for key, value in self.metadata.items():
            html += f'            <div class="metadata-item"><span class="metadata-label">{key.replace("_", " ").title()}:</span> {value}</div>\n'
        html += '        </div>\n'

        # Add sections
        for section in self.sections:
            severity_class = f' {section.severity}' if section.severity else ''
            html += f'        <div class="issue-card{severity_class}">\n'

            if section.severity:
                badge = f'<span class="badge {section.severity}">{section.severity}</span>'
                html += f'            <div class="issue-title">{badge} {section.title}</div>\n'
            else:
                html += f'            <h2>{section.title}</h2>\n'

            html += f'            {section.content}\n'
            html += '        </div>\n'

        # Footer
        html += f'''
        <div class="footer">
            <p>Generated by <strong>web-app-qa</strong> skill for Claude Skills</p>
            <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
'''

        return html

    def save(self, output_path: Path) -> None:
        """Save the report to a file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.generate())
        print(f"[✓] Report saved to {output_path}")


# Example usage
if __name__ == '__main__':
    # Example: Create a sample QA report
    report = HTMLReportGenerator(
        title="Example QA Test Report",
        description="Comprehensive quality assurance test results"
    )

    report.add_metadata('URL', 'https://example.com')
    report.add_metadata('Browser', 'Chrome 120.0')
    report.add_metadata('Environment', 'Staging')

    # Add summary
    summary_html = report.generate_summary_stats({
        'Total Tests': 25,
        'Passed': 20,
        'Failed': 3,
        'Warnings': 2
    })

    report.add_section(ReportSection(
        title="Test Summary",
        content=summary_html
    ))

    # Add critical issue
    report.add_section(ReportSection(
        title="Authentication Broken",
        content="<p>Login form is not submitting credentials correctly.</p>" +
                "<p><strong>Steps to reproduce:</strong></p>" +
                "<ol><li>Navigate to login page</li>" +
                "<li>Enter valid credentials</li>" +
                "<li>Click submit button</li>" +
                "<li>Observe: Page refreshes but user not logged in</li></ol>",
        severity="critical"
    ))

    # Save report
    report.save(Path('example_report.html'))
    print("\nExample report generated!")
