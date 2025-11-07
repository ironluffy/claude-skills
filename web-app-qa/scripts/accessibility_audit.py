#!/usr/bin/env python3
"""
Accessibility Audit Script - WCAG 2.1 AA/AAA compliance checking
Part of web-app-qa skill for Claude Skills

Usage:
    python accessibility_audit.py --url <url> --standard WCAG-AA --output report.html
    python accessibility_audit.py --url <url> --standard WCAG-AAA --include-screenshots
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page
from axe_core_python import AxeCore


class AccessibilityAuditor:
    """Performs comprehensive accessibility audits using axe-core"""

    WCAG_LEVELS = {
        'WCAG-A': ['wcag2a', 'wcag21a'],
        'WCAG-AA': ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'],
        'WCAG-AAA': ['wcag2a', 'wcag2aa', 'wcag2aaa', 'wcag21a', 'wcag21aa', 'wcag21aaa']
    }

    def __init__(self, url: str, standard: str = 'WCAG-AA', headless: bool = True):
        self.url = url
        self.standard = standard
        self.headless = headless
        self.results = None
        self.screenshot_path = None

    def run_audit(self, include_screenshots: bool = False) -> Dict:
        """Run accessibility audit on the page"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()

            print(f"[*] Navigating to {self.url}")
            page.goto(self.url)
            page.wait_for_load_state('networkidle')

            # Take screenshot if requested
            if include_screenshots:
                screenshot_dir = Path('screenshots')
                screenshot_dir.mkdir(exist_ok=True)
                self.screenshot_path = screenshot_dir / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=str(self.screenshot_path), full_page=True)
                print(f"[*] Screenshot saved: {self.screenshot_path}")

            # Run axe-core accessibility checks
            print(f"[*] Running {self.standard} accessibility audit...")
            axe = AxeCore(page)

            # Get tags for WCAG level
            tags = self.WCAG_LEVELS.get(self.standard, self.WCAG_LEVELS['WCAG-AA'])

            # Run scan
            results = axe.run(options={'runOnly': {'type': 'tag', 'values': tags}})

            browser.close()

        self.results = results
        return results

    def categorize_issues(self) -> Dict[str, List]:
        """Categorize issues by severity"""
        if not self.results:
            return {'critical': [], 'serious': [], 'moderate': [], 'minor': []}

        violations = self.results.get('violations', [])

        categorized = {
            'critical': [],
            'serious': [],
            'moderate': [],
            'minor': []
        }

        for violation in violations:
            impact = violation.get('impact', 'moderate')
            if impact == 'critical':
                categorized['critical'].append(violation)
            elif impact == 'serious':
                categorized['serious'].append(violation)
            elif impact == 'moderate':
                categorized['moderate'].append(violation)
            else:
                categorized['minor'].append(violation)

        return categorized

    def print_summary(self) -> None:
        """Print audit summary to console"""
        if not self.results:
            print("[!] No results available")
            return

        violations = self.results.get('violations', [])
        passes = self.results.get('passes', [])
        incomplete = self.results.get('incomplete', [])

        categorized = self.categorize_issues()

        print("\n" + "="*60)
        print(f"ACCESSIBILITY AUDIT SUMMARY - {self.standard}")
        print("="*60)
        print(f"URL: {self.url}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Critical issues
        if categorized['critical']:
            print(f"🚨 CRITICAL ISSUES ({len(categorized['critical'])}):")
            for issue in categorized['critical']:
                print(f"  - {issue['description']}")
                print(f"    Impact: {issue['impact']} | Affects {len(issue['nodes'])} element(s)")
            print()

        # Serious issues
        if categorized['serious']:
            print(f"⚠️  SERIOUS ISSUES ({len(categorized['serious'])}):")
            for issue in categorized['serious']:
                print(f"  - {issue['description']}")
                print(f"    Impact: {issue['impact']} | Affects {len(issue['nodes'])} element(s)")
            print()

        # Moderate/Minor warnings
        warning_count = len(categorized['moderate']) + len(categorized['minor'])
        if warning_count > 0:
            print(f"⚡ WARNINGS ({warning_count}):")
            for issue in categorized['moderate'][:3]:  # Show first 3
                print(f"  - {issue['description']}")
            if warning_count > 3:
                print(f"  ... and {warning_count - 3} more")
            print()

        # Passes
        print(f"✅ PASSED CHECKS: {len(passes)}")

        # Incomplete
        if incomplete:
            print(f"⏳ INCOMPLETE/MANUAL REVIEW NEEDED: {len(incomplete)}")

        print("="*60)

    def generate_html_report(self, output_path: Path) -> None:
        """Generate detailed HTML report"""
        if not self.results:
            print("[!] No results available for report generation")
            return

        violations = self.results.get('violations', [])
        passes = self.results.get('passes', [])
        incomplete = self.results.get('incomplete', [])
        categorized = self.categorize_issues()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Audit Report - {self.url}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 3px solid #0066cc; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .stat {{ display: inline-block; margin: 10px 20px 10px 0; }}
        .stat-label {{ font-weight: bold; }}
        .critical {{ background: #fee; border-left: 4px solid #d00; padding: 15px; margin: 15px 0; }}
        .serious {{ background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 15px 0; }}
        .moderate {{ background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 15px 0; }}
        .pass {{ color: #0a0; }}
        .issue-title {{ font-weight: bold; font-size: 1.1em; margin-bottom: 8px; }}
        .issue-description {{ color: #666; margin: 5px 0; }}
        .issue-help {{ background: #f9f9f9; padding: 10px; margin: 10px 0; border-radius: 4px; }}
        .wcag-tags {{ color: #0066cc; font-size: 0.9em; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
    </style>
</head>
<body>
    <h1>Accessibility Audit Report</h1>

    <div class="summary">
        <div class="stat"><span class="stat-label">URL:</span> {self.url}</div><br>
        <div class="stat"><span class="stat-label">Standard:</span> {self.standard}</div><br>
        <div class="stat"><span class="stat-label">Date:</span> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div><br>
        <hr style="margin: 15px 0;">
        <div class="stat"><span class="stat-label">🚨 Critical:</span> {len(categorized['critical'])}</div>
        <div class="stat"><span class="stat-label">⚠️  Serious:</span> {len(categorized['serious'])}</div>
        <div class="stat"><span class="stat-label">⚡ Moderate:</span> {len(categorized['moderate'])}</div>
        <div class="stat"><span class="stat-label">ℹ️  Minor:</span> {len(categorized['minor'])}</div>
        <div class="stat"><span class="stat-label pass">✅ Passed:</span> {len(passes)}</div>
    </div>
"""

        # Critical Issues
        if categorized['critical']:
            html += f"<h2>🚨 Critical Issues ({len(categorized['critical'])})</h2>"
            for issue in categorized['critical']:
                html += self._format_issue(issue, 'critical')

        # Serious Issues
        if categorized['serious']:
            html += f"<h2>⚠️  Serious Issues ({len(categorized['serious'])})</h2>"
            for issue in categorized['serious']:
                html += self._format_issue(issue, 'serious')

        # Moderate Issues
        if categorized['moderate']:
            html += f"<h2>⚡ Moderate Issues ({len(categorized['moderate'])})</h2>"
            for issue in categorized['moderate']:
                html += self._format_issue(issue, 'moderate')

        html += """
</body>
</html>
"""

        # Write report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)
        print(f"[✓] HTML report generated: {output_path}")

    def _format_issue(self, issue: Dict, severity: str) -> str:
        """Format a single issue for HTML report"""
        tags = ', '.join(issue.get('tags', []))
        node_count = len(issue.get('nodes', []))

        html = f"""
        <div class="{severity}">
            <div class="issue-title">{issue['description']}</div>
            <div class="issue-description">
                <strong>Impact:</strong> {issue['impact'].upper()} |
                <strong>Affects:</strong> {node_count} element(s)
            </div>
            <div class="wcag-tags">WCAG Tags: {tags}</div>
            <div class="issue-help">
                <strong>How to fix:</strong> {issue['help']}
                <br><a href="{issue['helpUrl']}" target="_blank">Learn more</a>
            </div>
"""

        # Add affected elements (first 3)
        if issue.get('nodes'):
            html += "<details><summary>Affected Elements</summary><ul>"
            for node in issue['nodes'][:3]:
                target = node.get('target', [''])[0]
                html_snippet = node.get('html', 'N/A')
                html += f"<li><code>{target}</code><br><pre>{html_snippet}</pre></li>"
            if len(issue['nodes']) > 3:
                html += f"<li>... and {len(issue['nodes']) - 3} more</li>"
            html += "</ul></details>"

        html += "</div>"
        return html


def main():
    parser = argparse.ArgumentParser(
        description='WCAG 2.1 AA/AAA accessibility compliance checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run WCAG 2.1 AA audit with HTML report
  python accessibility_audit.py \\
    --url https://app.example.com \\
    --standard WCAG-AA \\
    --output reports/a11y-report.html

  # Run AAA audit with screenshots
  python accessibility_audit.py \\
    --url https://app.example.com \\
    --standard WCAG-AAA \\
    --output reports/audit.html \\
    --include-screenshots

  # Run with browser visible
  python accessibility_audit.py \\
    --url https://app.example.com \\
    --no-headless
        """
    )

    parser.add_argument('--url', required=True, help='URL to audit')
    parser.add_argument('--standard', choices=['WCAG-A', 'WCAG-AA', 'WCAG-AAA'],
                       default='WCAG-AA', help='WCAG compliance level (default: WCAG-AA)')
    parser.add_argument('--output', type=Path, help='Output HTML report path')
    parser.add_argument('--include-screenshots', action='store_true',
                       help='Capture screenshots of issues')
    parser.add_argument('--no-headless', action='store_true', help='Show browser')

    args = parser.parse_args()

    try:
        auditor = AccessibilityAuditor(
            url=args.url,
            standard=args.standard,
            headless=not args.no_headless
        )

        auditor.run_audit(include_screenshots=args.include_screenshots)
        auditor.print_summary()

        if args.output:
            auditor.generate_html_report(args.output)

    except Exception as e:
        print(f"[✗] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
